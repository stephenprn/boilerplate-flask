from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required

from app.services import auth as service_auth

from ._common import to_dict

application_auth = Blueprint("application_auth", __name__)


@application_auth.route("/login", methods=["POST"])
@to_dict()
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    return service_auth.authenticate(email=email, password=password)


@application_auth.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    service_auth.register(email=email, username=username, password=password)

    return Response(status=200)


# this endpoint will return a 409 code if username is taken, 200 if not


@application_auth.route("/check-username", methods=["POST"])
def check_username():
    username = request.json.get("username")

    service_auth.check_username(username=username)

    return Response(status=200)


# this endpoint will return a 401 code if token is invalid, 200 if valid


@application_auth.route("/check-logged")
@jwt_required()
def check_logged():
    return Response(status=200)
