"""TR-064 service.

.. py::module:: tr064.service
   :synopsis: TR-064 service

.. moduleauthor:: Benjamin Füldner <benjamin@fueldner.net>
"""
from io import BytesIO
import lxml.etree as ET
import requests

from tr064.action import Action
from tr064.config import TR064_SERVICE_NAMESPACE
from tr064.exceptions import TR064UnknownActionException


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Service():
    """TR-064 service."""

    # pylint: disable=too-many-arguments
    def __init__(self, auth, base_url, service_type, service_id,
                 scpdurl, control_url, event_sub_url):
        self.auth = auth
        self.base_url = base_url
        self.service_type = service_type
        self.service_id = service_id
        self.scpdurl = scpdurl
        self.control_url = control_url
        self.event_sub_url = event_sub_url
        self.actions = {}

    def __getattr__(self, name):
        if name not in self.actions:
            self._fetch_actions(self.scpdurl)

        if name in self.actions:
            return self.actions[name]

        raise TR064UnknownActionException

    def _fetch_actions(self, scpdurl):
        """Fetch action description."""
        request = requests.get('{0}{1}'.format(self.base_url, scpdurl))
        if request.status_code == 200:
            xml = ET.parse(BytesIO(request.content))

            for action in xml.findall('./actionList/action', namespaces=TR064_SERVICE_NAMESPACE):
                name = action.findtext('name', namespaces=TR064_SERVICE_NAMESPACE)
                canonical_name = name.replace('-', '_')
                self.actions[canonical_name] = Action(
                    action,
                    self.auth,
                    self.base_url,
                    name,
                    self.service_type,
                    self.service_id,
                    self.control_url
                )
