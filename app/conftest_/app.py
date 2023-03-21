import os

import pytest

from app import create_app
from app.config import ENV_CONFIG_MAPPING
from app.enums.environment import Environment


@pytest.fixture(scope="session")
def app_fixture():
    database_name = f"{os.environ.get('POSTGRES_DB')}_test"

    # overriding database name in test config
    config = ENV_CONFIG_MAPPING[Environment.test]
    config.POSTGRES_DB = database_name

    db_url_parts = config.SQLALCHEMY_DATABASE_URI.split("/")
    db_url_parts[-1] = database_name

    config.SQLALCHEMY_DATABASE_URI = "/".join(db_url_parts)
    app = create_app(Environment.test)

    return app
