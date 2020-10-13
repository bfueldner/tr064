Examples
********

All devices and services used in the following examples are taken from the `TR-064 Description XML <https://192.168.178.1:49443/tr64desc.xml>`_. Used actions are described in the XML refered with the ``SCPDURL`` element of each service. More details about the action can be obtained from the router manufacturer.

Devices/Services/Actions:

* :ref:`InternetGatewayDevice`
    * :ref:`DeviceInfo`
        * :ref:`GetInfo`
        * :ref:`GetSecurityPort`
* :ref:`LANDevice`
    * :ref:`Hosts`
        * :ref:`GetHostNumberOfEntries_GetGenericHostEntry`
    * :ref:`WLANConfiguration`
        * :ref:`GetInfo_SetEnable`

.. _InternetGatewayDevice:

InternetGatewayDevice
=====================

.. _DeviceInfo:

DeviceInfo
----------

Support ``urn:DeviceInfo-com:serviceId:DeviceInfo1``.

.. _GetInfo:

GetInfo
~~~~~~~

Getting router information::

    res = client.InternetGatewayDevice.DeviceInfo.GetInfo()
    print('ManufacturerName', res.NewManufacturerName)
    print('ManufacturerOUI', res.NewManufacturerOUI)
    print('ModelName', res.NewModelName)
    print('Description', res.NewDescription)

.. _GetSecurityPort:

GetSecurityPort
~~~~~~~~~~~~~~~

Get port for secure access::

    unsafe_client = tr064.Client('username', 'password', 'http://192.168.178.1:49000')
    res = unsafe_client.InternetGatewayDevice.DeviceInfo.GetSecurityPort()

    safe_client = tr064.Client('username', 'password', 'https://192.168.178.1:{}'.format(res.NewSecurityPort))

.. _LANDevice:

LANDevice
=========

.. _Hosts:

Hosts
-----

.. _GetHostNumberOfEntries_GetGenericHostEntry:

GetHostNumberOfEntries/GetGenericHostEntry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List all assigned network devices::

    number_of_entries = client.LANDevice.Hosts.GetHostNumberOfEntries()
    for index in range(int(number_of_entries.NewHostNumberOfEntries)):
        host = client.LANDevice.Hosts.GetGenericHostEntry(NewIndex=index)
        print(host.NewIPAddress, host.NewMACAddress, host.NewHostName)

.. _WLANConfiguration:

WLANConfiguration
-----------------

.. _GetInfo_SetEnable:

GetInfo/SetEnable
~~~~~~~~~~~~~~~~~

Enable third WLAN device if not enabled::

    info = client.LANDevice.WLANConfiguration[2].GetInfo()
    if not bool(info.NewEnable):
        client.LANDevice.WLANConfiguration[2].SetEnable(NewEnable=1)
