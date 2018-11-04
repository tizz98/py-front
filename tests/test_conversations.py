import tempfile


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
