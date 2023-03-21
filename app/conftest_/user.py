from unittest import mock

import pytest

from app.models.user import User


@pytest.fixture
@mock.patch("app.models._common.uuid4", return_value="test-uuid")
@mock.patch(
    "app.models.user.hash_password",
    return_value=("test-password-hash", "test-password-salt"),
)
def test_user(mock_uuid, mock_hash_password, db_session):
    user = User(username="test_user", email="test@test.com", password="password")

    db_session.add(user)
    db_session.flush()

    return user
