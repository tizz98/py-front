class TestTeamListing:
    def test_team_has_id(self, api):
        teams = api.teams()
        assert teams[0].id == "tim_55c8c149"

    def test_team_has_name(self, api):
        teams = api.teams()
        assert teams[0].name == "Delivery"

    def test_teams_are_iterable(self, api):
        teams = api.teams()
        assert len(teams) == 1
        assert list(teams)


class TestTeamRetrieval:
    def test_team_has_id(self, api):
        team = api.team("tim_55c8c149")
        assert team.id == "tim_55c8c149"

    def test_team_has_name(self, api):
        team = api.team("tim_55c8c149")
        assert team.name == "Delivery"

    def test_team_has_inboxes(self, api):
        team = api.team("tim_55c8c149")
        assert list(team.inboxes)

    def test_team_has_members(self, api):
        team = api.team("tim_55c8c149")
        assert list(team.members)
