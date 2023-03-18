from marshmallow import EXCLUDE, fields, validate

from ._common import CamelCaseSchema


class LoginBodySchema(CamelCaseSchema):
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(6, 30))

    class Meta:
        unknown = EXCLUDE


class UsernameBodySchema(CamelCaseSchema):
    username = fields.Str(required=True, validate=validate.Length(4, 20))

    class Meta:
        unknown = EXCLUDE


class RegisterBodySchema(LoginBodySchema, UsernameBodySchema):
    pass
