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
    def test_channel_has_id(self, api):
        channels = api.inbox_channels("inb_55c8c149")
        assert channels[0].id == "cha_55c8c149"

    def test_channel_has_type(self, api):
        channels = api.inbox_channels("inb_55c8c149")
        assert channels[0].type == "smtp"

    def test_channels_are_iterable(self, api):
        channels = api.inbox_channels("inb_55c8c149")
        assert len(channels) == 1
        assert list(channels)


class TestInboxConversationListing:
    def test_conversation_has_id(self, api):
        convos = api.inbox_conversations("inb_55c8c149")
        assert convos[0].id == "cnv_55c8c149"

    def test_conversation_has_status(self, api):
        convos = api.inbox_conversations("inb_55c8c149")
        assert convos[0].status == "archived"

    def test_conversations_are_iterable(self, api):
        convos = api.inbox_conversations("inb_55c8c149")
        assert len(convos) == 1
        assert list(convos)


class TestInboxTeammateListing:
    def test_teammate_has_id(self, api):
        teammates = api.inbox_teammates("inb_55c8c149")
        assert teammates[0].id == "tea_55c8c149"

    def test_teammate_has_email(self, api):
        teammates = api.inbox_teammates("inb_55c8c149")
        assert teammates[0].email == "leela@planet-express.com"

    def test_teammates_are_iterable(self, api):
        teammates = api.inbox_teammates("inb_55c8c149")
        assert len(teammates) == 1
        assert list(teammates)