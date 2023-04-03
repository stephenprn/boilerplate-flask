import json
import os
import traceback
from typing import Dict, List, Optional, Union

from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from app.config import ENV_CONFIG_MAPPING
from app.database import db
from app.enums.environment import Environment
from app.errors import BUSINESS_ERRORS
from app.utils.json import CustomJSONEncoder, snake_to_camel_case


def create_app(environment: Optional[Environment] = None) -> Flask:
    app = Flask(__name__)

    init_config(app, environment)
    app.json_encoder = CustomJSONEncoder
    db.init_app(app)

    with app.app_context():
        register_blueprints(app)
        register_errorhandlers(app)
        register_request_hooks(app)
        register_commands(app)

        db.create_all()  # Create sql tables for our data models

        CORS(app, resources={r"/*": {"origins": "*"}})
        JWTManager(app)

        migrate = Migrate(app, db)
        migrate.init_app(app)

    return app


def init_config(app: Flask, environment: Optional[Environment] = None):
    if not environment:
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

    config = ENV_CONFIG_MAPPING[environment]

    app.config.from_object(config)


def register_blueprints(app: Flask):
    from app.routes.auth import application_auth
    from app.routes.user import application_user

    app.register_blueprint(application_auth, url_prefix="/auth")
    app.register_blueprint(application_user, url_prefix="/user")


def register_errorhandlers(app: Flask):
    error_message_key = app.config["ERROR_MESSAGE_KEY"]

    def render_error_business(err):
        error_response = {error_message_key: err.message}

        if err.detail:
            error_response["detail"] = err.detail

        return jsonify(error_response), err.code

    def render_error_default(err):
        if isinstance(err, HTTPException):
            return jsonify({error_message_key: err.description}), err.code or 500

        error_response: Dict[str, Union[str, List[str]]] = {error_message_key: "Internal server error"}

        # if DEBUG, we specify full stack trace
        if app.config.get("DEBUG"):
            error_response["detail"] = traceback.format_exc().split("\n")

        return jsonify(error_response), 500

    for error_type in BUSINESS_ERRORS:
        app.register_error_handler(error_type, render_error_business)

    # default handler: internal server error and werkzeug exceptions
    app.register_error_handler(Exception, render_error_default)


def register_request_hooks(app: Flask):
    @app.after_request
    def after_request(response: Response):
        if response.is_json:
            response.set_data(json.dumps(snake_to_camel_case(response.get_json())))

        return response


def register_commands(app: Flask):
    from app.commands.user import user_cli

    app.cli.add_command(user_cli)
