import datetime
from enum import Enum
from json import JSONEncoder
from typing import Dict, List, Union

from app.utils.string import camel_case


def snake_to_camel_case(input_object: Union[Dict, List]) -> Union[Dict, List]:
    if isinstance(input_object, list):
        camel_list = []

        for item in input_object:
            if isinstance(item, list) or isinstance(item, dict):
                camel_list.append(snake_to_camel_case(item))
            else:
                camel_list.append(item)

        return camel_list

    camel_dict = {}

    for key, value in input_object.items():
        if isinstance(value, dict):
            value = snake_to_camel_case(value)
        elif isinstance(value, list):
            value = snake_to_camel_case(value)

        camel_dict[camel_case(key)] = value

    return camel_dict


def default_handler(value) -> str:
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    elif isinstance(value, Enum):
        return value.name

    raise TypeError("Unknown type")


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return default_handler(obj)
        except TypeError:
            pass

        return JSONEncoder.default(self, obj)
