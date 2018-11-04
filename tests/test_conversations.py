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
