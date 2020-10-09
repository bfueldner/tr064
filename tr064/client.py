"""TR-064 client."""
from io import BytesIO
import lxml.etree as ET
import requests
from requests.auth import HTTPDigestAuth

DEVICE_NAMESPACE = {
    '': 'urn:dslforum-org:device-1-0'
}

SERVICE_NAMESPACE = {
    '': 'urn:dslforum-org:service-1-0'
}

class AttributeDict(dict):
    """Direct access dict entries like attributes."""

    def __getattr__(self, name):
        return self[name]


class Action():
    """TR-064 action."""

    def __init__(self, auth, base_url, name, _type, _id, control_url, xml):
        self.auth = auth
        self.base_url = base_url
        self.name = name
        self.type = _type
        self.id = _id
        self.control_url = control_url

        ET.register_namespace('s', 'http://schemas.xmlsoap.org/soap/envelope/')
        ET.register_namespace('h', 'http://soap-authentication.org/digest/2001/10/')

        self.headers = {'content-type': 'text/xml; charset="utf-8"'}
        self.envelope = ET.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope', attrib={'{http://schemas.xmlsoap.org/soap/envelope/}encodingStyle': 'http://schemas.xmlsoap.org/soap/encoding/'})
        self.body = ET.SubElement(self.envelope, '{http://schemas.xmlsoap.org/soap/envelope/}Body')

        self.in_arguments = {}
        self.out_arguments = {}

        for argument in xml.findall('./argumentList/argument', namespaces=SERVICE_NAMESPACE):
            name = argument.findtext('name', namespaces=SERVICE_NAMESPACE)
            direction = argument.findtext('direction', namespaces=SERVICE_NAMESPACE)

            if direction == 'in':
                self.in_arguments[name.replace('-', '_')] = name

            if direction == 'out':
                self.out_arguments[name] = name.replace('-', '_')

    def __call__(self, **kwargs):
        missing_arguments = self.in_arguments.keys() - kwargs.keys()
        unknown_arguments = kwargs.keys() - self.in_arguments.keys()
        if missing_arguments:
            raise AttributeError('Missing argument(s) \''+"', '".join(missing_arguments)+'\'')

        if unknown_arguments:
            raise AttributeError('Unknown argument(s) \''+"', '".join(unknown_arguments)+'\'')

        # Add SOAP action to header
        self.headers['soapaction'] = '"{}#{}"'.format(self.type, self.name)
        ET.register_namespace('u', self.type)

        # Prepare body for request
        self.body.clear()
        action = ET.SubElement(self.body, '{{{}}}{}'.format(self.type, self.name))
        for key in kwargs:
            arg = ET.SubElement(action, self.in_arguments[key])
            arg.text = str(kwargs[key])

        # soap._InitChallenge(header)
        data = ET.tostring(self.envelope, encoding='utf-8', xml_declaration=True).decode()
        request = requests.post('{0}{1}'.format(self.base_url, self.control_url),
                                headers=self.headers,
                                auth=self.auth,
                                data=data
                               )
        if request.status_code != 200:
            return request.status_code

        # Translate response and prepare dict
        xml = ET.parse(BytesIO(request.content))
        response = AttributeDict()
        for arg in list(xml.find('.//{{{}}}{}Response'.format(self.type, self.name))):
            name = self.out_arguments[arg.tag]
            response[name] = arg.text
        return response


class Service():
    """TR-064 service."""

    def __init__(self, auth, base_url, _type, _id, scpdurl, control_url, event_sub_url):
        self.auth = auth
        self.base_url = base_url
        self.type = _type
        self.id = _id
        self.scpdurl = scpdurl
        self.control_url = control_url
        self.event_sub_url = event_sub_url
        self.actions = {}

    def __getattr__(self, name):
        if name not in self.actions:
            self._FetchActions(self.scpdurl)

        if name in self.actions:
            return self.actions[name]
        return None

    def _FetchActions(self, scpdurl):
        request = requests.get('{0}{1}'.format(self.base_url, scpdurl))
        if request.status_code == 200:
            xml = ET.parse(BytesIO(request.content))

            for action in xml.findall('./actionList/action', namespaces=SERVICE_NAMESPACE):
                name = action.findtext('name', namespaces=SERVICE_NAMESPACE)
                canonical_name = name.replace('-', '_')
                self.actions[canonical_name] = Action(self.auth, self.base_url, name, self.type, self.id, self.control_url, action)


class ServiceList(list):
    """Direct access to first list entry."""

    def __getattr__(self, name):
        return self[0].__getattr__(name)


class Device():
    """TR-064 device."""

    def __init__(self, auth, base_url, xml_node):
        self.services = {}

        for service in xml_node.findall('./serviceList/service', namespaces=DEVICE_NAMESPACE):
            _type = service.findtext('serviceType', namespaces=DEVICE_NAMESPACE)
            _id = service.findtext('serviceId', namespaces=DEVICE_NAMESPACE)
            control_url = service.findtext('controlURL', namespaces=DEVICE_NAMESPACE)
            event_sub_url = service.findtext('eventSubURL', namespaces=DEVICE_NAMESPACE)
            scpdurl = service.findtext('SCPDURL', namespaces=DEVICE_NAMESPACE)

            name = _type.split(':')[-2].replace('-', '_')
            if name not in self.services:
                self.services[name] = ServiceList()
            self.services[name].append(
                Service(auth, base_url, _type, _id, scpdurl, control_url, event_sub_url)
            )

    def __getattr__(self, name):
        if name in self.services:
            return self.services[name]
        return None


class Client():
    """TR-064 client."""

    def __init__(self, user, password, base_url='https://fritz.box:49443'):
        self.base_url = base_url
        self.auth = HTTPDigestAuth(user, password)

        self.devices = {}

    def __getattr__(self, name):
        if name not in self.devices:
            self._FetchDevices()

        if name in self.devices:
            return self.devices[name]
        return None

    def keys(self):
        return self.devices.keys()

    def _FetchDevices(self, description_file='/tr64desc.xml'):
        request = requests.get('{0}{1}'.format(self.base_url, description_file))
        if request.status_code == 200:
            xml = ET.parse(BytesIO(request.content))

            for device in xml.findall('.//device', namespaces=DEVICE_NAMESPACE):
                name = device.findtext('deviceType', namespaces=DEVICE_NAMESPACE).split(':')[-2]
                if not name in self.devices:
                    self.devices[name] = Device(self.auth, self.base_url, device)
