from datetime import datetime

from app.repositories._common.base import RepositoryBase
from app.repositories._common.order_by import OrderBy
from app.types.result import ResultWithNbr


class TestRepositoryCommon:
    def test_repository_base(self, ModelBaseTest, db_session):
        model_base_test_one = ModelBaseTest(test_property_str="one", test_property_int=1)
        model_base_test_one.creation_date = datetime(2011, 1, 1)
        model_base_test_two = ModelBaseTest(test_property_str="two", test_property_int=2)
        model_base_test_two.creation_date = datetime(2012, 1, 1)
        model_base_test_three = ModelBaseTest(test_property_str="three", test_property_int=3)
        model_base_test_three.creation_date = datetime(2013, 1, 1)
        model_base_test_four = ModelBaseTest(test_property_str="four", test_property_int=4)
        model_base_test_four.creation_date = datetime(2014, 1, 1)

        db_session.add(model_base_test_one)
        db_session.add(model_base_test_two)
        db_session.add(model_base_test_three)
        db_session.add(model_base_test_four)

        db_session.flush()

        class RepositoryBaseTest(RepositoryBase[ModelBaseTest]):
            model = ModelBaseTest

        repo_base_test = RepositoryBaseTest()

        assert repo_base_test.list_(
            order_creation_date=OrderBy.ASC,
        ) == [model_base_test_one, model_base_test_two, model_base_test_three, model_base_test_four]

        assert repo_base_test.list_with_nbr_results(
            filter_uuid_in=[model_base_test_one.uuid, model_base_test_two.uuid],
            filter_id_in=[model_base_test_two.id, model_base_test_three.id],
        ) == ResultWithNbr(total=1, data=[model_base_test_two])

        assert (
            repo_base_test.count(
                filter_id_in=[
                    model_base_test_four.id,
                    model_base_test_three.id,
                    model_base_test_one.id
                    + model_base_test_two.id
                    + model_base_test_three.id
                    + model_base_test_four.id,
                ]
            )
            == 2
        )

        assert not repo_base_test.exists(
            filter_id_in=[
                model_base_test_one.id + model_base_test_two.id + model_base_test_three.id + model_base_test_four.id
            ]
        )
        assert repo_base_test.exists(filter_uuid_in=[model_base_test_one.uuid])

        assert repo_base_test.get(filter_uuid_in=[model_base_test_one.uuid]) == model_base_test_one
