import os

from flask.cli import AppGroup

import app.services.auth as service_auth
from app.errors import BadRequestError
from app.repositories.user import UserRepository

user_cli = AppGroup("user")

repo_user = UserRepository()


@user_cli.command("init_admin", help="Create an admin user based on ADMIN_EMAIL and ADMIN_PASSWORD env variables")
def init_admin():
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_password or not admin_email:
        raise BadRequestError("ADMIN_PASSWORD and ADMIN_EMAIL env variables must be set to run this command")

    if repo_user.exists(filter_email_in=[admin_email]):
        return

    service_auth.register(email=admin_email, username="admin", password=admin_password)
