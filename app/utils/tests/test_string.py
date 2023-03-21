import app.utils.string as util_string


class TestUtilJson:
    def test_camel_case(self):
        assert util_string.snake_to_camel_case("chien") == "chien"
        assert util_string.snake_to_camel_case("oui_bonjour") == "ouiBonjour"
        assert util_string.snake_to_camel_case("ceci__est_un___test") == "ceciEstUnTest"
