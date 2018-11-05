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
