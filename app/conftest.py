import os
from typing import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.orm.session import Session

from app import create_app
from app.config import ENV_CONFIG_MAPPING
from app.database import db
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


def teardown_db(db):
    db.session.remove()
    db.drop_all()


def clean_db():
    for table in reversed(db.metadata.sorted_tables):
        schema = table.schema if table.schema else "public"

        db.session.execute(text(f'DELETE FROM {schema}."{table.name}"'))
    db.session.commit()


@pytest.fixture(scope="session")
def db_fixture(app_fixture):
    yield db

    with app_fixture.app_context():
        teardown_db(db)


@pytest.fixture(scope="function")
def db_session(db_fixture, app_fixture) -> Generator[Session, None, None]:
    with app_fixture.app_context():
        clean_db()
        yield db.session
        db.session.rollback()
