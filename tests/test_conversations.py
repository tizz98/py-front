import json
import tempfile

from front.api import Status
from front.marshalling import detect_encoding


class TestConversationListing:
    def test_conversation_has_id(self, api):
        convos = api.conversations()
        assert convos[0].id == "cnv_55c8c149"

    def test_conversation_has_subject(self, api):
        convos = api.conversations()
        assert convos[0].subject == "You broke my heart, Hubert."

    def test_conversations_are_iterable(self, api):
        convos = api.conversations()
        assert len(convos) == 1
        assert list(convos)


class TestConversationRetrieval:
    def test_conversation_has_id(self, api):
        conv = api.conversation("cnv_55c8c149")
        assert conv.id == "cnv_55c8c149"

    def test_conversation_has_subject(self, api):
        conv = api.conversation("cnv_55c8c149")
        assert conv.subject == "You broke my heart, Hubert."

    def test_conversation_has_assignee(self, api):
        conv = api.conversation("cnv_55c8c149")
        assert conv.assignee.username == "leela"


class TestAttachments:
    def test_download_attachment(self, api):
        conv = api.conversation("cnv_55c8c149")
        url = conv.last_message.attachments[0].url

        file_name = tempfile.mktemp()

        api.download_attachment(url, file_name)

        with open(file_name, 'rb') as f:
            assert len(f.read()) > 0

    def test_headers_are_correct(self, api):
        conv = api.conversation("cnv_55c8c149")
        url = conv.last_message.attachments[0].url

        api.download_attachment(url, tempfile.mktemp())

        headers = api._requester.calls[0].request.headers

        assert 'Content-Type' not in headers
        assert 'Accept' not in headers


class TestConversationInboxListing:
    def test_inbox_has_id(self, api):
        inboxes = api.conversation_inboxes("cnv_55c8c149")
        assert inboxes[0].id == "inb_55c8c149"

    def test_inbox_has_name(self, api):
        inboxes = api.conversation_inboxes("cnv_55c8c149")
        assert inboxes[0].name == "Team"

    def test_inbox_has_is_private(self, api):
        inboxes = api.conversation_inboxes("cnv_55c8c149")
        assert inboxes[0].is_private is False

    def test_inboxes_are_iterable(self, api):
        inboxes = api.conversation_inboxes("cnv_55c8c149")
        assert len(inboxes) == 1
        assert list(inboxes)


class TestConversationFollowerListing:
    def test_follower_has_id(self, api):
        followers = api.conversation_followers("cnv_55c8c149")
        assert followers[0].id == "tea_55c8c149"

    def test_follower_has_username(self, api):
        followers = api.conversation_followers("cnv_55c8c149")
        assert followers[0].username == "leela"

    def test_followers_are_iterable(self, api):
        followers = api.conversation_followers("cnv_55c8c149")
        assert len(followers) == 1
        assert list(followers)


class TestConversationEventListing:
    def test_event_has_id(self, api):
        events = api.conversation_events("cnv_55c8c149")
        assert events[0].id == "evt_55c8c149"

    def test_event_has_type(self, api):
        events = api.conversation_events("cnv_55c8c149")
        assert events[0].type == "assign"

    def test_event_has_target(self, api):
        events = api.conversation_events("cnv_55c8c149")
        assert events[0].target._meta['type'] == "teammate"
        assert events[0].target.id == "tea_55c8c149"

    def test_events_are_iterable(self, api):
        events = api.conversation_events("cnv_55c8c149")
        assert len(events) == 1
        assert list(events)


class TestConversationMessageListing:
    def test_message_has_id(self, api):
        messages = api.conversation_messages("cnv_55c8c149")
        assert messages[0].id == "msg_55c8c149"

    def test_message_has_blurb(self, api):
        messages = api.conversation_messages("cnv_55c8c149")
        assert messages[0].blurb == "Anything less than immortality is a..."

    def test_messages_are_iterable(self, api):
        messages = api.conversation_messages("cnv_55c8c149")
        assert len(messages) == 1
        assert list(messages)


class TestConversationUpdating:
    def test_http_method_is_correct(self, api):
        api.update_conversation("cnv_55c8c149", updates={
            "assignee_id": "tea_55c8c149",
            "inbox_id": "inb_128yew",
            "status": Status.DELETED.value,
            "tags": ["fun", "delivery"],
        })

        req = api._requester.calls[0].request

        assert req.method == 'PATCH'

    def test_json_body_is_correct(self, api):
        api.update_conversation("cnv_55c8c149", updates={
            "assignee_id": "tea_55c8c149",
            "inbox_id": "inb_128yew",
            "status": Status.DELETED.value,
            "tags": ["fun", "delivery"],
        })

        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
            "assignee_id": "tea_55c8c149",
            "inbox_id": "inb_128yew",
            "status": Status.DELETED.value,
            "tags": ["fun", "delivery"],
        }
