from typing import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.orm.session import Session

from app.database import db


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
