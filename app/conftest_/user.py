from unittest import mock

import pytest

from app.enums.user import UserRole
from app.models.user import User


@pytest.fixture
@mock.patch("app.models._common.uuid4", return_value="test-uuid")
@mock.patch(
    "app.utils.hash.os.urandom",
    return_value=b"\xb0\xd0h\x13\xcc\xd0\xdc\x06\xa6\x0e\xa4T\xcb\xa7\xb0\xcb\xe3\x0bp\xb5Oe\xca\xe3\x8fF&\xb3\xdb+\xe9\x1b",
)
def test_user(mock_uuid, mock_hash_password, db_session):
    user = User(username="test_user", email="test@test.com", password="password")

    db_session.add(user)
    db_session.flush()

    return user


@pytest.fixture
@mock.patch("app.models._common.uuid4", return_value="test-uuid-admin")
@mock.patch(
    "app.utils.hash.os.urandom",
    return_value=b"]z\x00ds`k\xd4\x87n\xe1\xfd[z\xf9-Us\\\xd4\xe8R\x88\x15l5\xa1?\xf0\x9c\xd2*",
)
def test_admin(mock_uuid, mock_hash_password, db_session):
    user = User(username="test_admin", email="admin@test.com", password="password", role=UserRole.ADMIN)

    db_session.add(user)
    db_session.flush()

    return user
