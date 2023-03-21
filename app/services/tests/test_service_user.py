import app.services.user as service_user


class TestServiceUser:
    def test_list_(self, db_session):
        assert service_user.list_(nbr_results=10, page_nbr=0) == []
