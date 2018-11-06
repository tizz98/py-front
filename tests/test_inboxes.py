class TestInboxListing:
    def test_inbox_has_id(self, api):
        inboxes = api.inboxes()
        assert inboxes[0].id == "inb_55c8c149"

    def test_listing_by_teammate_id(self, api):
        inboxes = api.teammate_inboxes("tea_55c8c149")
        assert inboxes[0].id == "inb_55c8c149"

    def test_listing_by_team_id(self, api):
        inboxes = api.team_inboxes("tim_55c8c149")
        assert inboxes[0].id == "inb_55c8c149"


class TestInboxCreation:
    pass


class TestInboxRetrieval:
    pass


class TestInboxChannelListing:
    pass


class TestInboxConversationListing:
    pass


class TestInboxTeammateListing:
    pass
