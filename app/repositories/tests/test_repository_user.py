from datetime import datetime

from app.enums.user import UserRole
from app.models.user import User
from app.repositories._common.order_by import OrderBy
from app.repositories.user import UserRepository
from app.types.result import ResultWithNbr


class TestRepositoriesUserCommon:
    def test_repository_user(self, db_session):
        user_one = User(
            username="user_one",
            email="user_one@test.com",
            password="password_one",
            role=UserRole.USER,
        )
        user_one.creation_date = datetime(2011, 1, 1)
        user_two = User(
            username="user_two",
            email="user_two@test.com",
            password="password_two",
            role=UserRole.USER,
        )
        user_two.creation_date = datetime(2012, 1, 1)
        user_three = User(
            username="user_three",
            email="user_three@test.com",
            password="password_three",
            role=UserRole.ADMIN,
        )
        user_three.creation_date = datetime(2013, 1, 1)

        db_session.add(user_one)
        db_session.add(user_two)
        db_session.add(user_three)

        db_session.flush()

        repo_user = UserRepository()

        assert repo_user.list_(
            filter_email_in=["user_two@test.com", "not_existing@test.com"],
            order_creation_date=OrderBy.ASC,
        ) == [user_two]

        assert repo_user.list_with_nbr_results(
            filter_username_in=["user_one", "user_three"],
            order_creation_date=OrderBy.DESC,
        ) == ResultWithNbr(total=2, data=[user_three, user_one])
