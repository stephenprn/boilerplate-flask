from functools import wraps
from typing import Any, Callable, Dict, List, Type, Union

from flask import request
from marshmallow import Schema, ValidationError

from app.enums.user import UserRole
from app.errors import BadRequestError, ForbiddenError
from app.routes.validators.pagination import PaginationParamsSchema
from app.services import auth as service_auth
from app.utils.mixin import SerializableMixin

# routes annotations


def paginated(nbr_results_max=100) -> Callable:
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            pagination_params_schema = PaginationParamsSchema(context={"nbr_results_max": nbr_results_max})

            try:
                pagination_params: Any = pagination_params_schema.load(request.args)
            except ValidationError as err:
                raise BadRequestError(
                    "Missing or incorrect query params",
                    detail={"body": err.normalized_messages()},
                )

            kwargs_paginated = {**kwargs, **pagination_params}

            return function(*args, **kwargs_paginated)

        wrapper.__name__ = function.__name__
        return wrapper

    return decorator


def has_role(roles: List[UserRole]) -> Callable:
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if service_auth.get_current_identity().role not in roles:
                raise ForbiddenError("You are not allowed to access this resource")

            return function(*args, **kwargs)

        wrapper.__name__ = function.__name__
        return wrapper

    return decorator


def to_dict() -> Callable:
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            output = function(*args, **kwargs)

            if _check_type(output, SerializableMixin):
                output_dict = _serialize(output)
            elif _check_type(output, dict):
                output_dict = output
            else:
                output_dict = dict(output)

            return output_dict

        wrapper.__name__ = function.__name__
        return wrapper

    return decorator


def body_validation(validator: Type[Schema], **kwargs_validator):
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if request.json is None:
                raise BadRequestError("Body not found")

            schema = validator(**kwargs_validator)

            try:
                body = schema.load(request.json)
            except ValidationError as err:
                raise BadRequestError(
                    "Missing or incorrect body values",
                    detail={"body": err.normalized_messages()},
                )

            return function(*args, **kwargs, body=body)

        wrapper.__name__ = function.__name__
        return wrapper

    return decorator


# helpers


def _serialize(data: SerializableMixin) -> Union[Dict, List[Dict]]:
    if isinstance(data, list):
        data_dict = [item.serialize() for item in data]
    else:
        data_dict = data.serialize()

    return data_dict


def _check_type(item, type_):
    return isinstance(item, type_) or isinstance(item, list) and [isinstance(elt, type_) for elt in item]
