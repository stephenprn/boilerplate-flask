from app.enums.user import UserRole
from app.models.user import User


class TestModelUser:
    def test_user(self, test_user, db_session):
        users = User.query.filter(User.username == test_user.username).all()

        assert len(users) == 1

        user = users[0]

        assert user.username == test_user.username
        assert user.email == test_user.email
        assert user.role == UserRole.USER
        assert user.password_hashed == "test-password-hash"
        assert user.password_salt == "test-password-salt"

        assert repr(user) == (
            "<users username='test_user' email='test@test.com' role=<UserRole.USER: 10> "
            f"password_hashed='test-password-hash' password_salt='test-password-salt' id={user.id} uuid='test-uuid' "
            f"creation_date={repr(user.creation_date)} update_date={repr(user.update_date)}>"
        )

        assert user.serialize() == {
            "creation_date": user.creation_date,
            "email": "test@test.com",
            "role": UserRole.USER,
            "update_date": user.update_date,
            "username": "test_user",
            "uuid": "test-uuid",
        }
