from marshmallow import EXCLUDE, fields, validate

from ._common import CamelCaseSchema


class PaginationParamsSchema(CamelCaseSchema):
    nbr_results = fields.Int(required=True, validate=validate.Range(min=1, max=20))
    page_nbr = fields.Int(required=True, validate=validate.Range(min=0))

    class Meta:
        unknown = EXCLUDE
