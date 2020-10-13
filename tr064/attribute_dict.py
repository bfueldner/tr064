"""TR-064 attribute dict.

.. py::module:: tr064.attribute_dict
   :synopsis: TR-064 attribute dict

.. moduleauthor:: Benjamin Füldner <benjamin@fueldner.net>
"""


class AttributeDict(dict):
    """Direct access dict entries like attributes."""

    def __getattr__(self, name):
        return self[name]
