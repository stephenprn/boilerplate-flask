from marshmallow import EXCLUDE, ValidationError, fields, validate, validates_schema

from ._common import CamelCaseSchema


class PaginationParamsSchema(CamelCaseSchema):
    nbr_results = fields.Int(required=True, validate=validate.Range(min=1))
    page_nbr = fields.Int(required=True, validate=validate.Range(min=0))

    @validates_schema
    def validates_schema(self, data, **kwargs):
        nbr_results_max = self.context["nbr_results_max"]

        if data["nbr_results"] > nbr_results_max:
            raise ValidationError(
                {"nbrResults": f"Must be greater than or equal to 1 and less than or equal to {nbr_results_max}."}
            )

    class Meta:
        unknown = EXCLUDE
