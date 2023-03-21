import os
from unittest import mock

from app.commands.user import init_admin


class TestCommandsUser:
    @mock.patch("app.services.auth.register", autospec=True)
    def test_init_admin(self, mock_register, db_session, app_fixture):
        runner = app_fixture.test_cli_runner()

        # ADMIN_PASSWORD and ADMIN_EMAIL not set

        with mock.patch.dict("os.environ"):
            del os.environ["ADMIN_PASSWORD"]
            del os.environ["ADMIN_EMAIL"]

            runner.invoke(init_admin)
            mock_register.assert_not_called()

        # ADMIN_PASSWORD and ADMIN_EMAIL well set

        with mock.patch.dict(
            "app.services.auth.os.environ",
            {"ADMIN_EMAIL": "admin@test.com", "ADMIN_PASSWORD": "admin_password"},
        ):
            runner.invoke(init_admin)
            mock_register.assert_called_once_with(email="admin@test.com", username="admin", password="admin_password")
