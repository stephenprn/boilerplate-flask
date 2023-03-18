import json
import os
import traceback
from typing import Dict, List, Union

from flask import Flask, Response, jsonify
from flask_alembic import Alembic
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import CONFIGS
from app.database import db
from app.enums.environment import Environment
from app.errors import BUSINESS_ERRORS
from app.services.auth import init_admin
from app.utils.json import CustomJSONEncoder, snake_to_camel_case


def create_app() -> Flask:
    app = Flask(__name__)

    init_config(app)
    app.json_encoder = CustomJSONEncoder
    db.init_app(app)

    with app.app_context():
        register_blueprints(app)
        register_errorhandlers(app)
        register_request_hooks(app)

        db.create_all()  # Create sql tables for our data models

        init_admin()

        CORS(app)
        JWTManager(app)

        alembic = Alembic()
        alembic.init_app(app)

    return app


def init_config(app: Flask):
    environment_str = os.environ.get("ENVIRONMENT")

    if not environment_str:
        raise Exception("ENVIRONMENT env var must be specified")

    try:
        environment = Environment[environment_str]
    except KeyError:
        raise Exception(
            f"""ENVIRONMENT env var can take value: {
                ",".join([env.name for env in Environment])
            } | current value: {environment_str}"""
        )

    environment_config_mapping = {config.ENVIRONMENT: config for config in CONFIGS}
    config = environment_config_mapping[environment]

    app.config.from_object(config)


def register_blueprints(app: Flask):
    from app.routes.auth import application_auth
    from app.routes.user import application_user

    app.register_blueprint(application_auth, url_prefix="/auth")
    app.register_blueprint(application_user, url_prefix="/user")


def register_errorhandlers(app: Flask):
    error_message_key = app.config["ERROR_MESSAGE_KEY"]

    def render_error_business(err):
        error_code = getattr(err, "code")
        error_response = {error_message_key: err.message}

        if err.detail:
            error_response["detail"] = err.detail

        return jsonify(error_response), error_code

    def render_error_default(err):
        error_response: Dict[str, Union[str, List[str]]] = {error_message_key: "Internal server error"}

        # if DEBUG, we specify full stack trace
        if app.config.get("DEBUG"):
            error_response["detail"] = traceback.format_exc().split("\n")

        return jsonify(error_response), 500

    for error_type in BUSINESS_ERRORS:
        app.register_error_handler(error_type, render_error_business)

    # default handler
    app.register_error_handler(Exception, render_error_default)


def register_request_hooks(app: Flask):
    @app.after_request
    def after_request(response: Response):
        if response.is_json:
            response.set_data(json.dumps(snake_to_camel_case(response.get_json())))

        return response
