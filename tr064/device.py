"""."""

from tr064.config import TR064_DEVICE_NAMESPACE
from tr064.exceptions import TR064UnknownServiceException
from tr064.service import Service
from tr064.service_list import ServiceList


# pylint: disable=too-few-public-methods
class Device():
    """TR-064 device.

    :param lxml.etree.Element xml:
        XML device element
    :param HTTPBasicAuthHandler auth:
        HTTPBasicAuthHandler object, e.g. HTTPDigestAuth
    :param str base_url:
        URL to router.
    """

    def __init__(self, xml, auth, base_url):
        self.services = {}

        for service in xml.findall('./serviceList/service', namespaces=TR064_DEVICE_NAMESPACE):
            service_type = service.findtext('serviceType', namespaces=TR064_DEVICE_NAMESPACE)
            service_id = service.findtext('serviceId', namespaces=TR064_DEVICE_NAMESPACE)
            control_url = service.findtext('controlURL', namespaces=TR064_DEVICE_NAMESPACE)
            event_sub_url = service.findtext('eventSubURL', namespaces=TR064_DEVICE_NAMESPACE)
            scpdurl = service.findtext('SCPDURL', namespaces=TR064_DEVICE_NAMESPACE)

            name = service_type.split(':')[-2].replace('-', '_')
            if name not in self.services:
                self.services[name] = ServiceList()

            self.services[name].append(
                Service(
                    auth,
                    base_url,
                    service_type,
                    service_id,
                    scpdurl,
                    control_url,
                    event_sub_url
                )
            )

    def __getattr__(self, name):
        if name in self.services:
            return self.services[name]

        raise TR064UnknownServiceException
