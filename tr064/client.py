"""TR-064 client.

.. py::module:: tr064.client
   :synopsis: TR-064 client

.. moduleauthor:: Benjamin Füldner <benjamin@fueldner.net>
"""
from io import BytesIO
import lxml.etree as ET
import requests
from requests.auth import HTTPDigestAuth

from tr064.config import TR064_DEVICE_NAMESPACE
from tr064.exceptions import TR064UnknownDeviceException
from tr064.device import Device


# pylint: disable=too-few-public-methods
class Client():
    """TR-064 client."""

    def __init__(self, user, password, base_url='https://fritz.box:49443'):
        self.base_url = base_url
        self.auth = HTTPDigestAuth(user, password)

        self.devices = {}

    def __getattr__(self, name):
        if name not in self.devices:
            self._fetch_devices()

        if name in self.devices:
            return self.devices[name]

        raise TR064UnknownDeviceException

    def _fetch_devices(self, description_file='/tr64desc.xml'):
        """Fetch device description."""
        request = requests.get(
            '{0}{1}'.format(self.base_url, description_file))

        if request.status_code == 200:
            xml = ET.parse(BytesIO(request.content))

            for device in xml.findall('.//device', namespaces=TR064_DEVICE_NAMESPACE):
                name = device.findtext('deviceType',
                                       namespaces=TR064_DEVICE_NAMESPACE).split(':')[-2]

                if name not in self.devices:
                    self.devices[name] = Device(self.auth, self.base_url, device)
