import json

from front.marshalling import detect_encoding


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

    def test_inboxes_are_iterable(self, api):
        inboxes = api.inboxes()
        assert len(inboxes) == 1
        assert list(inboxes)


class TestInboxCreation:
    _data = {
        "name": "Delivery Support",
        "teammate_ids": ["tea_55c8c149"],
    }

    def test_http_method_is_correct(self, api):
        api.create_inbox(self._data)
        method = api._requester.calls[0].request.method

        assert method == 'POST'

    def test_http_method_is_correct_when_creating_teammate_inbox(self, api):
        api.create_teammate_inbox("tea_55c8c149", self._data)
        method = api._requester.calls[0].request.method

        assert method == 'POST'

    def test_http_method_is_correct_when_creating_team_inbox(self, api):
        api.create_team_inbox("tim_55c8c149", self._data)
        method = api._requester.calls[0].request.method

        assert method == 'POST'

    def test_json_body_is_correct(self, api):
        api.create_inbox(self._data)
        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
            "name": "Delivery Support",
            "teammate_ids": ["tea_55c8c149"],
        }

    def test_json_body_is_correct_when_creating_teammate_inbox(self, api):
        api.create_teammate_inbox("tea_55c8c149", self._data)
        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
           "name": "Delivery Support",
           "teammate_ids": ["tea_55c8c149"],
       }

    def test_json_body_is_correct_when_creating_team_inbox(self, api):
        api.create_team_inbox("tim_55c8c149", self._data)
        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
           "name": "Delivery Support",
           "teammate_ids": ["tea_55c8c149"],
       }

    def test_response_has_id(self, api):
        inbox = api.create_inbox(self._data)
        assert inbox.id == "inb_55c8c149"

    def test_response_has_name(self, api):
        inbox = api.create_inbox(self._data)
        assert inbox.name == "Delivery support"


class TestInboxRetrieval:
    def test_inbox_has_id(self, api):
        inbox = api.inbox("inb_55c8c149")
        assert inbox.id == "inb_55c8c149"

    def test_inbox_has_name(self, api):
        inbox = api.inbox("inb_55c8c149")
        assert inbox.name == "Team"


class TestInboxChannelListing:
    pass


class TestInboxConversationListing:
    pass


class TestInboxTeammateListing:
    pass
