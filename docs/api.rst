TR-064 API
**********

General usage
=============

Create a client connection to the router::

    import tr064

    client = tr064.Client('username', 'password', 'http://192.168.178.1:49000')

    res = client.InternetGatewayDevice.DeviceInfo.GetInfo()
    print(res.NewManufacturerName)

Actions (functions) are executed by append ``device``, ``service`` and ``action`` to the client:

    ``Client.DeviceName.ServiceName.ActionName(Arguments, ...)``

If a service is offered multiple times, actions can be accessed by the zero-based square bracket operator:

    ``Client.DeviceName.ServiceName[1].ActionName(Arguments, ...)``

See more :doc:`examples`.

.. note::

    If services, actions or arguments contain a minus sign ``-``, it must be replaced with an underscore ``_`` and vice versa.

API
===

Client
------

.. autoclass:: tr064.client.Client

Exceptions
----------

.. automodule:: tr064.exceptions
    :members: TR064Exception, TR064UnknownDeviceException, TR064UnknownServiceException, TR064UnknownServiceIndexException, TR064UnknownActionException, TR064UnknownArgumentException, TR064MissingArgumentException

.. note::

    All following classes are never used directly! They are only documented for the sake of completeness.

Device
------

.. autoclass:: tr064.device.Device

Service
-------

.. autoclass:: tr064.service.Service

Action
------

.. autoclass:: tr064.action.Action

Helper
------

.. autoclass:: tr064.attribute_dict.AttributeDict
.. autoclass:: tr064.service_list.ServiceList
