from unittest import mock

import app.utils.hash as util_hash


class TestUtilHash:
    @mock.patch("app.utils.hash.os.urandom", return_value=b"\xe2\xaf\xbc:\xdd")
    def test_hash_password(self, mock_urandom):
        assert util_hash.hash_password("test-password") == (
            "" "b'fN8Arx7SLe1cMV7TZVTLklgsepQnNpgqEKMqUS0s2t4='",
            "b'4q+8Ot0='",
        )

    def test_check_password(self):
        password_hashed, salt = util_hash.hash_password("test-password")

        assert util_hash.check_password(password_input="test-password", salt=salt, password_hashed=password_hashed)
