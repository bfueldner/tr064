"""Test TR-064 client.

.. module:: test.test_client
   :synopsis: TR-064 client test

.. moduleauthor:: Benjamin Füldner <benjamin@fueldner.net>
"""

import os
import unittest
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import tr064


class TR064Server(BaseHTTPRequestHandler):
    """TR-064 server mock."""

    # pylint: disable=redefined-builtin
    def log_message(self, format, *args):
        return

    # pylint: disable=invalid-name
    def do_GET(self):
        """HTTP GET handler."""
        url = urlparse(self.path)
        filename = os.path.abspath(os.path.join('res', url.path.lstrip('/')))

        if os.path.isfile(filename):
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml')
            self.end_headers()

            with open(filename) as file:
                self.wfile.write(file.read().encode())
            return

        self.send_response(404)
        self.end_headers()

    # pylint: disable=invalid-name
    def do_POST(self):
        """HTTP POST handler."""
        url = urlparse(self.path)
        _, action = self.headers['soapaction'].strip('"').split('#')
        filename = os.path.abspath(os.path.join('res', url.path.lstrip('/'), action))

        if os.path.isfile(filename):
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml')
            self.end_headers()

            with open(filename) as file:
                self.wfile.write(file.read().encode())
            return

        self.send_response(404)
        self.end_headers()


class TestClient(unittest.TestCase):
    """Test class tr064.client.Client."""

    @classmethod
    def setUpClass(cls):
        """Set-up test server."""
        cls._server = HTTPServer(('localhost', 49000), TR064Server)
        cls._server_thread = threading.Thread(target=cls._server.serve_forever)
        cls._server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """Tear-down test server."""
        cls._server.shutdown()
        cls._server.server_close()
        cls._server_thread.join()

    def setUp(self):
        """Set-up client."""
        self.client = tr064.Client('username', 'password', 'http://localhost:49000')

    def test_unknown_device(self):
        """Test unknown device."""

        with self.assertRaises(tr064.exceptions.TR064UnknownDeviceException):
            self.client.UnknownDevice.UnknownService.UnknownAction()

    def test_unknown_service(self):
        """Test unknown service."""

        with self.assertRaises(tr064.exceptions.TR064UnknownServiceException):
            self.client.InternetGatewayDevice.UnknownService.UnknownAction()

    def test_unknown_service_index(self):
        """Test unknown service index."""

        with self.assertRaises(tr064.exceptions.TR064UnknownServiceIndexException):
            self.client.InternetGatewayDevice.DeviceInfo[1].UnknownAction()

    def test_unknown_action(self):
        """Test unknown action."""

        with self.assertRaises(tr064.exceptions.TR064UnknownActionException):
            self.client.InternetGatewayDevice.DeviceInfo.UnknownAction()

    def test_unknown_argument(self):
        """Test unknown argument."""

        with self.assertRaises(tr064.exceptions.TR064UnknownArgumentException):
            self.client.InternetGatewayDevice.DeviceInfo.GetSecurityPort(UnknownArgument=1)

    def test_missing_argument(self):
        """Test missing argument."""

        with self.assertRaises(tr064.exceptions.TR064MissingArgumentException):
            self.client.LANDevice.WLANConfiguration[0].SetEnable()

    def test_status_code(self):
        """Test status code."""

        res = self.client.LANDevice.Hosts.GetHostNumberOfEntries()
        self.assertIsNotNone(res)
        self.assertEqual(res, 404)

    def test_get_action(self):
        """Test get action."""

        res = self.client.InternetGatewayDevice.DeviceInfo.GetSecurityPort()
        self.assertIsNotNone(res)
        self.assertEqual(int(res.NewSecurityPort), 49443)

    def test_set_action(self):
        """Test set action."""

        res = self.client.LANDevice.Hosts.GetGenericHostEntry(NewIndex=1)
        self.assertIsNotNone(res)
        self.assertEqual(res.NewIPAddress, '192.168.179.1')
        self.assertEqual(res.NewAddressSource, 'DHCP')
        self.assertEqual(res.NewMACAddress, 'AA:BB:CC:DD:EE:FF')
        self.assertEqual(res.NewInterfaceType, 'Ethernet')
