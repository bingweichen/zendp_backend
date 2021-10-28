from datetime import datetime, date
from decimal import Decimal


class DictMixin(object):
    """docstring for DictMixin"""

    @staticmethod
    def to_dict(cls, exclude=[]):

        attrs = cls if isinstance(cls, dict) else cls.__dict__
        attrs_dict = {}
        for key, value in attrs.items():
            if key.startswith('_') or key in exclude:
                pass
            elif isinstance(value, Decimal):
                attrs_dict[key] = float(value)
            elif isinstance(value, datetime):
                attrs_dict[key] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                attrs_dict[key] = date.strftime(value, '%Y-%m-%d')
            else:
                attrs_dict[key] = value

        return attrs_dict

    @staticmethod
    def from_dict(cls, attrs):
        """
        set the attributes of the cls.
        Also, will create a new instance if not an instance be provided
        """
        if isinstance(cls, type):
            cls_instance = cls()
        else:
            cls_instance = cls

        for key, value in attrs.items():
            if hasattr(cls_instance, key):
                setattr(cls_instance, key, value)

        return cls_instance
