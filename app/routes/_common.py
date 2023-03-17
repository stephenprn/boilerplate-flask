from functools import wraps
from typing import Callable, Dict, List, Union

from flask import request

from app.enums.user import UserRole
from app.errors import BadRequestError, ForbiddenError
from app.services import auth as service_auth
from app.utils.mixin import SerializableMixin

# routes annotations


def paginated(nbr_results_max=100) -> Callable:
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                page_nbr = int(request.args.get("page_nbr"))
            except (ValueError, TypeError):
                raise BadRequestError("Page number is required: page_nbr")

            try:
                nbr_results = max(int(request.args.get("nbr_results")), 0)
                nbr_results = min(int(request.args.get("nbr_results")), nbr_results_max)
            except (ValueError, TypeError):
                nbr_results = nbr_results_max

            kwargs["nbr_results"] = nbr_results
            kwargs["page_nbr"] = page_nbr

            return function(*args, **kwargs)

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


# helpers


def _serialize(data: SerializableMixin) -> Union[Dict, List[Dict]]:
    if isinstance(data, list):
        data_dict = [item.serialize() for item in data]
    else:
        data_dict = data.serialize()

    return data_dict


def _check_type(item, type_):
    return isinstance(item, type_) or isinstance(item, list) and [isinstance(elt, type_) for elt in item]
