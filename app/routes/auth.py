from typing import Dict

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from app.routes.validators.auth import LoginBodySchema, RegisterBodySchema, UsernameBodySchema
from app.services import auth as service_auth

from ._common import body_validation, to_dict

application_auth = Blueprint("application_auth", __name__)


@application_auth.route("/login", methods=["POST"])
@body_validation(LoginBodySchema)
@to_dict()
def login(body: Dict):
    return service_auth.authenticate(**body)


@application_auth.route("/register", methods=["POST"])
@body_validation(RegisterBodySchema)
def register(body: Dict):
    service_auth.register(**body)

    return Response(status=200)


# this endpoint will return a 409 code if username is taken, 200 if not


@application_auth.route("/check-username", methods=["POST"])
@body_validation(UsernameBodySchema)
def check_username(body: Dict):
    service_auth.check_username(**body)

    return Response(status=200)


# this endpoint will return a 401 code if token is invalid, 200 if valid


@application_auth.route("/check-logged")
@jwt_required()
def check_logged():
    return Response(status=200)
