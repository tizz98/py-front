class TestTopicConversationList:
    def test_conversations_are_iterable(self, api):
        convos = api.topic_conversations('top_55c8c149')
        assert list(convos)
        assert len(convos) == 1

    def test_conversation_has_id(self, api):
        convos = api.topic_conversations('top_55c8c149')
        assert convos[0].id == "cnv_55c8c149"

    def test_conversation_has_tags(self, api):
        convos = api.topic_conversations('top_55c8c149')
        assert list(convos[0].tags)
