from typing import Optional
from unittest import mock

from app.database import db
from app.models._common import ModelBase


class TestModelsCommon:
    @mock.patch("app.models._common.uuid4", return_value="test-uuid")
    def test_model_base(self, mock_uuid, db_fixture, db_session):
        class ModelBaseTest(ModelBase):
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

        db_fixture.create_all()

        model_base_test = ModelBaseTest(test_property_str="test string", test_property_int=12)

        assert (
            model_base_test.__repr__()
            == "<model_base_test test_property_str='test string' test_property_int=12 id=<deferred> uuid=<deferred> creation_date=<deferred> update_date=<deferred>>"
        )

        db_session.add(model_base_test)
        db_session.commit()

        test_results = ModelBaseTest.query.filter(ModelBaseTest.test_property_int == 12).all()

        assert len(test_results) == 1

        test_result = test_results[0]

        assert test_result.test_property_str == "test string"
        assert test_result.test_property_int == 12
        assert test_result.uuid == "test-uuid"

        assert test_result.serialize() == {
            "creation_date": test_result.creation_date,
            "test_property_int": 12,
            "test_property_str": "test string",
            "update_date": test_result.update_date,
            "uuid": "test-uuid",
        }

        assert test_result.serialize(
            exclude_cols=["update_date", "test_property_int"],
        ) == {
            "creation_date": test_result.creation_date,
            "id": test_result.id,
            "test_property_str": "test string",
            "uuid": "test-uuid",
        }

        assert test_result.serialize(
            include_cols=["test_property_str", "uuid"],
        ) == {
            "test_property_str": "test string",
            "uuid": "test-uuid",
        }

        assert test_result.serialize(
            exclude_cols=["update_date", "test_property_int"],
            include_cols=["update_date", "test_property_str", "uuid"],
        ) == {
            "test_property_str": "test string",
            "uuid": "test-uuid",
        }
