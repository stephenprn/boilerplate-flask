from datetime import datetime
from enum import Enum

import app.utils.json as util_json


class TestEnum(Enum):
    TEST_A = "test_a"
    TEST_B = "test_b"


JSON_EXAMPLE = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 35,
    "email_address": "john.doe@example.com",
    "phone_numbers": [
        {
            "type": "home",
            "number": "555-1234",
            "extra_detail": {
                "extra_detail": True,
                "more_infos": {
                    "origin": "french",
                    "extra_elements": ["yes", "this_is_a_test"],
                },
            },
        },
        {"type": "work", "number": "555-5678"},
    ],
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "country": "USA",
    },
    "extra_datetime": datetime(2020, 1, 1),
    "extra_enum": TestEnum.TEST_A,
}


class TestUtilJson:
    def test_snake_to_camel_case(self):
        assert util_json.snake_to_camel_case(JSON_EXAMPLE) == {
            "address": {
                "city": "Anytown",
                "country": "USA",
                "state": "CA",
                "street": "123 Main St",
                "zipCode": "12345",
            },
            "age": 35,
            "emailAddress": "john.doe@example.com",
            "extraDatetime": datetime(2020, 1, 1, 0, 0),
            "extraEnum": TestEnum.TEST_A,
            "firstName": "John",
            "lastName": "Doe",
            "phoneNumbers": [
                {
                    "extraDetail": {
                        "extraDetail": True,
                        "moreInfos": {
                            "extraElements": [
                                "yes",
                                "this_is_a_test",
                            ],
                            "origin": "french",
                        },
                    },
                    "number": "555-1234",
                    "type": "home",
                },
                {
                    "number": "555-5678",
                    "type": "work",
                },
            ],
        }
