from abc import ABC
from typing import Dict

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.models.user import User


@pytest.fixture
def client(app_fixture: Flask):
    with app_fixture.test_client() as client:
        yield client


class ApiTest(ABC):
    BASE_URL = "/"

    client: FlaskClient
    test_user: User
    test_admin: User
    email_access_token_mapping: Dict[str, str]

    @pytest.fixture(autouse=True)
    def setup(self, client, test_admin, test_user):
        self.client = client
        self.test_admin = test_admin
        self.test_user = test_user

        self.email_access_token_mapping = {}

    @property
    def client_unthenticated(self) -> FlaskClient:
        self.client.environ_base["HTTP_AUTHORIZATION"] = ""

        return self.client

    @property
    def client_auth_user(self) -> FlaskClient:
        if not self.email_access_token_mapping.get(self.test_user.email):
            response = self.client.post(
                "/auth/login",
                json={"email": self.test_user.email, "password": "password"},
            )

            assert response.status_code == 200
            assert response.json
            assert response.json.get("accessToken")

            self.email_access_token_mapping[self.test_user.email] = response.json["accessToken"]

        self.client.environ_base[
            "HTTP_AUTHORIZATION"
        ] = f"Bearer {self.email_access_token_mapping[self.test_user.email]}"

        return self.client

    @property
    def client_auth_admin(self) -> FlaskClient:
        if not self.email_access_token_mapping.get(self.test_admin.email):
            response = self.client.post(
                "/auth/login",
                json={"email": self.test_admin.email, "password": "password"},
            )

            assert response.status_code == 200
            assert response.json
            assert response.json.get("accessToken")

            self.email_access_token_mapping[self.test_admin.email] = response.json["accessToken"]

        self.client.environ_base[
            "HTTP_AUTHORIZATION"
        ] = f"Bearer {self.email_access_token_mapping[self.test_admin.email]}"

        return self.client
