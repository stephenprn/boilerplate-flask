from typing import Optional

import pytest
from sqlalchemy import inspect

from app.database import db
from app.models._common import ModelBase


@pytest.fixture(scope="function")
def ModelBaseTest(app_fixture, db_fixture):
    table_name = "model_base_test"

    with app_fixture.app_context():
        # model may have been defined in a previous test: we need to set extend_existing to true if already defined
        table_exists = inspect(db_fixture.engine).dialect.has_table(db_fixture.engine.connect(), table_name)

    class ModelBaseTest(ModelBase):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": table_exists}

        test_property_str = db.Column(db.String)
        test_property_int = db.Column(db.Integer)

        def __init__(
            self,
            test_property_str: Optional[str] = None,
            test_property_int: Optional[int] = None,
        ):
            super().__init__()

            self.test_property_str = test_property_str
            self.test_property_int = test_property_int

    with app_fixture.app_context():
        db_fixture.create_all()

    return ModelBaseTest
