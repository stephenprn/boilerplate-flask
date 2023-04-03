from unittest import mock

from app.conftest_.client import ApiTest


class TestRouteAuth(ApiTest):
    BASE_URL = "/user"

    def test_list(self):
        # admin can list users

        response = self.client_auth_admin.get(f"{self.BASE_URL}/", query_string={"pageNbr": 0, "nbrResults": 10})

        assert response.status_code == 200
        assert response.json == [
            {
                "creationDate": mock.ANY,
                "email": "admin@test.com",
                "role": "ADMIN",
                "updateDate": mock.ANY,
                "username": "test_admin",
                "uuid": "test-uuid-admin",
            },
            {
                "creationDate": mock.ANY,
                "email": "test@test.com",
                "role": "USER",
                "updateDate": mock.ANY,
                "username": "test_user",
                "uuid": "test-uuid",
            },
        ]

        # unauthenticated user can't list users

        response = self.client_unthenticated.get(f"{self.BASE_URL}/", query_string={"pageNbr": 0, "nbrResults": 10})

        assert response.status_code == 401

        # regular user can't list users

        response = self.client_auth_user.get(f"{self.BASE_URL}/", query_string={"pageNbr": 0, "nbrResults": 10})

        assert response.status_code == 403

    def test_get(self, test_user):
        # admin can get user

        response = self.client_auth_admin.get(f"{self.BASE_URL}/{test_user.uuid}")

        assert response.status_code == 200
        assert response.json == {
            "creationDate": mock.ANY,
            "email": "test@test.com",
            "role": "USER",
            "updateDate": mock.ANY,
            "username": "test_user",
            "uuid": "test-uuid",
        }

        # unauthenticated user can't get user

        response = self.client_unthenticated.get(f"{self.BASE_URL}/{test_user.uuid}")

        assert response.status_code == 401

        # regular user can't get user

        response = self.client_auth_user.get(f"{self.BASE_URL}/{test_user.uuid}")

        assert response.status_code == 403
