import os
from typing import Dict, TypedDict

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from app.database import db
from app.errors import BadRequestError, ConflictError, UnauthorizedError
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.hash import check_password

repo_user = UserRepository()


class UserAuth(TypedDict):
    access_token: str
    refresh_token: str
    user: Dict


def register(email: str, username: str, password: str):
    email = email.lower().strip()

    if repo_user.exists(filter_email_in=[email]):
        raise ConflictError("This email is already registered")

    check_username(username=username)

    user = User(
        username=username,
        email=email,
        password=password,
    )

    db.session.add(user)
    db.session.commit()


def check_username(username: str):
    if repo_user.exists(filter_username_in=[username]):
        raise ConflictError("This username is already taken")


# flask_jwt_extended functions


def authenticate(email: str, password: str) -> UserAuth:
    email = email.lower().strip()

    user = repo_user.get(filter_email_in=[email])

    if not user or not check_password(
        password_input=password,
        salt=user.password_salt,
        password_hashed=user.password_hashed,
    ):
        raise UnauthorizedError("Invalid credentials")

    user_dict = user.serialize(include_cols=["username", "uuid"])

    return UserAuth(
        access_token=create_access_token(identity=user_dict),
        refresh_token=create_refresh_token(identity=user_dict),
        user=user_dict,
    )


def get_current_identity() -> User:
    identity_dict = get_jwt_identity()
    user_uuid = identity_dict.get("uuid")

    user = repo_user.get(filter_uuid_in=[user_uuid])

    if not user:
        raise UnauthorizedError("Invalid token")

    return user


# init methods


def init_admin():
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_password or not admin_email:
        raise BadRequestError("ADMIN_PASSWORD and ADMIN_EMAIL must be set as env var when no admin is set in db")

    if repo_user.exists(filter_email_in=[admin_email]):
        return

    register(email=admin_email, username="admin", password=admin_password)
