from typing import Dict, List, Optional, Type


class BusinessError(Exception):
    code: int
    _message: str
    detail: Optional[Dict]

    def __init__(self, *args, **kwargs):
        if not args:
            raise ValueError("You must specify a message for this exception")

        self._message = args[0]
        self.detail = kwargs.get("detail")

    @property
    def message(self):
        return str(self._message)


class BadRequestError(BusinessError):
    code = 400


class UnauthorizedError(BusinessError):
    code = 401


class ForbiddenError(BusinessError):
    code = 403


class ConflictError(BusinessError):
    code = 409


BUSINESS_ERRORS: List[Type[BusinessError]] = [BadRequestError, UnauthorizedError, ForbiddenError, ConflictError]
