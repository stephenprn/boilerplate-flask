from unittest import mock


class TestModelsCommon:
    @mock.patch("app.models._common.uuid4", return_value="test-uuid")
    def test_model_base(self, mock_uuid, ModelBaseTest, db_session):
        model_base_test = ModelBaseTest(test_property_str="test string", test_property_int=12)

        db_session.add(model_base_test)
        db_session.flush()

        test_results = ModelBaseTest.query.filter(ModelBaseTest.test_property_int == 12).all()

        assert len(test_results) == 1

        test_result = test_results[0]

        assert test_result.test_property_str == "test string"
        assert test_result.test_property_int == 12
        assert test_result.uuid == "test-uuid"

        assert repr(test_result) == (
            "<model_base_test test_property_str='test string' test_property_int=12"
            f" id=1 uuid='test-uuid' creation_date={repr(test_result.creation_date)} update_date={repr(test_result.update_date)}>"
        )

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
