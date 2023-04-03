from unittest import mock

import pytest

import app.services.auth as service_auth
from app.errors import ConflictError, UnauthorizedError
from app.models.user import User


class TestServiceAuth:
    @mock.patch("app.models._common.uuid4", return_value="test-uuid")
    @mock.patch(
        "app.models.user.hash_password",
        return_value=("test-password-hash", "test-password-salt"),
    )
    def test_register(self, mock_uuid, mock_hash_password, db_session):
        # register test user

        service_auth.register(email="test@test.com", username="test_user", password="password")

        users = User.query.filter(User.email == "test@test.com").all()

        assert len(users) == 1

        user = users[0]

        assert user.email == "test@test.com"
        assert user.username == "test_user"
        assert user.password_hashed == "test-password-hash"
        assert user.password_salt == "test-password-salt"

        # try to register user with same email as test user

        with pytest.raises(ConflictError, match="This email is already registered"):
            service_auth.register(email="test@test.com", username="test_user_two", password="password")

        # try to register user with same username as test user

        with pytest.raises(ConflictError, match="This username is already taken"):
            service_auth.register(email="test_two@test.com", username="test_user", password="password")

    def test_check_username(self, test_user):
        # no exception is raised because username is not registered

        service_auth.check_username(username="not_existing_user")

        # exception is raised because username is registered

        with pytest.raises(ConflictError, match="This username is already taken"):
            service_auth.check_username(username="test_user")

    def test_authenticate(self, test_user):
        # authenticate with right credentials

        with mock.patch(
            "app.services.auth.check_password",
            return_value=True,
        ):
            user_auth = service_auth.authenticate(email="test@test.com", password="password")

            assert user_auth == {
                "access_token": mock.ANY,
                "refresh_token": mock.ANY,
                "user": {"username": "test_user", "uuid": test_user.uuid},
            }
            assert type(user_auth["access_token"]) == str
            assert type(user_auth["refresh_token"]) == str

        # authenticate with wrong password

        with pytest.raises(UnauthorizedError, match="Invalid credentials"):
            service_auth.authenticate(email="test@test.com", password="password_wrong")

        # authenticate with not existing email

        with pytest.raises(UnauthorizedError, match="Invalid credentials"):
            service_auth.authenticate(email="test_not_existing@test.com", password="password")

    @mock.patch("app.services.auth.get_jwt_identity", return_value={"uuid": "test-uuid"})
    def test_get_current_identity(self, mock_get_jwt_identity, db_session):
        # get current identity with not existing user (real-life usecase: user has been deleted)

        with pytest.raises(UnauthorizedError, match="Invalid token"):
            service_auth.get_current_identity()

        user = User(username="test_user", email="test@test.com", password="password")
        user.uuid = "test-uuid"
        db_session.add(user)
        db_session.flush()

        assert service_auth.get_current_identity() == user
