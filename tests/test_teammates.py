import json

from front.marshalling import detect_encoding


class TestTeammateListing:
    def test_teammate_has_id(self, api):
        teammates = api.teammates()
        assert teammates[0].id == "tea_55c8c149"

    def test_teammate_has_email(self, api):
        teammates = api.teammates()
        assert teammates[0].email == "leela@planet-express.com"

    def test_teammates_are_iterable(self, api):
        teammates = api.teammates()
        assert len(teammates) == 1
        assert list(teammates)


class TestTeammateRetrieval:
    def test_teammate_has_id(self, api):
        teammate = api.teammate("tea_55c8c149")
        assert teammate.id == "tea_55c8c149"

    def test_teammate_has_email(self, api):
        teammate = api.teammate("tea_55c8c149")
        assert teammate.email == "leela@planet-express.com"


class TestTeammateUpdate:
    def test_http_method_is_correct(self, api):
        api.update_teammate("tea_55c8c149", updates={
            "username": "fry",
            "first_name": "Philip",
            "last_name": "Fry",
            "is_admin": True,
            "is_available": False,
        })

        req = api._requester.calls[0].request

        assert req.method == 'PATCH'

    def test_json_body_is_correct(self, api):
        api.update_teammate("tea_55c8c149", updates={
            "username": "fry",
            "first_name": "Philip",
            "last_name": "Fry",
            "is_admin": True,
            "is_available": False,
        })

        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
            "username": "fry",
            "first_name": "Philip",
            "last_name": "Fry",
            "is_admin": True,
            "is_available": False,
        }
