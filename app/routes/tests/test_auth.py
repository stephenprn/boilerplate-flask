from app.conftest_.client import ApiTest


class TestRouteAuth(ApiTest):
    BASE_URL = "/auth"

    def test_register(self):
        # non-existing user

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/register",
            json={
                "email": "test_bis@test.com",
                "password": "test_password",
                "username": "test_bis",
            },
        )

        assert response.status_code == 200

        # existing email

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/register",
            json={
                "email": "test_bis@test.com",
                "password": "test_password",
                "username": "test_bis_",
            },
        )

        assert response.status_code == 409
        assert response.json == {"message": "This email is already registered"}

        # existing username

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/register",
            json={
                "email": "test_bis_@test.com",
                "password": "test_password",
                "username": "test_bis",
            },
        )

        assert response.status_code == 409
        assert response.json == {"message": "This username is already taken"}

        # no body provided

        response = self.client_unthenticated.post(f"{self.BASE_URL}/register", json={})

        assert response.status_code == 400
        assert response.json == {"message": "Body not found"}

        # wrongbody provided

        response = self.client_unthenticated.post(f"{self.BASE_URL}/register", json={"email": "test@test.com"})

        assert response.status_code == 400
        assert response.json == {
            "detail": {
                "body": {
                    "password": [
                        "Missing data for required field.",
                    ],
                    "username": [
                        "Missing data for required field.",
                    ],
                },
            },
            "message": "Missing or incorrect body values",
        }

    def test_login(self, test_user):
        # right credentials

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/login",
            json={
                "email": test_user.email,
                "password": "password",
            },
        )

        assert response.status_code == 200
        assert response.json

        assert response.json["accessToken"]
        assert response.json["refreshToken"]
        assert response.json["user"] == {"username": "test_user", "uuid": "test-uuid"}

        # wrong password

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/login",
            json={
                "email": test_user.email,
                "password": "wrong_password",
            },
        )
        assert response.status_code == 401
        assert response.json == {"message": "Invalid credentials"}

        # not existing email

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/login",
            json={
                "email": f"wrong_{test_user.email}",
                "password": "wrong_password",
            },
        )
        assert response.status_code == 401
        assert response.json == {"message": "Invalid credentials"}

    def test_check_username(self, test_user):
        # existing username

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/check-username",
            json={"username": test_user.username},
        )

        assert response.status_code == 409
        assert response.json == {"message": "This username is already taken"}

        # non-existing username

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/check-username",
            json={"username": "non_existing"},
        )

        assert response.status_code == 200

        # too long username

        response = self.client_unthenticated.post(
            f"{self.BASE_URL}/check-username",
            json={"username": "too_longgggg_username"},
        )

        assert response.status_code == 400
        assert response.json == {
            "detail": {"body": {"username": ["Length must be between 4 and 20."]}},
            "message": "Missing or incorrect body values",
        }

    def test_check_logged(self):
        response = self.client_auth_user.get(f"{self.BASE_URL}/check-logged")
        assert response.status_code == 200

        response = self.client_auth_admin.get(f"{self.BASE_URL}/check-logged")
        assert response.status_code == 200

        response = self.client_unthenticated.get(f"{self.BASE_URL}/check-logged")
        assert response.status_code == 401
