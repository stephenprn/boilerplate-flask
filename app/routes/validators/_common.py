from marshmallow import Schema

from app.utils.string import camel_case


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camel_case(field_obj.data_key or field_name)
