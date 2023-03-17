from typing import Optional

from app.errors import BadRequestError


def check_length(
    text: str,
    name: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
):
    if text is None:
        raise BadRequestError(f"{name} must be specified")

    if min_length is not None and len(text) < min_length:
        raise BadRequestError(400, f"{name} must be at least {min_length} characters long")

    if max_length is not None and len(text) > max_length:
        raise BadRequestError(400, f"{name} must be no more than {min_length} characters long")
