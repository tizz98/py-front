class TestEventListing:
    def test_event_has_id(self, api):
        events = api.events()
        assert events[0].id == "evt_55c8c149"

    def test_event_has_type(self, api):
        events = api.events()
        assert events[0].type == "assign"

    def test_events_are_iterable(self, api):
        events = api.events()
        assert len(events) == 1
        assert list(events)


class TestEventRetrieval:
    def test_event_has_id(self, api):
        event = api.event("evt_55c8c149")
        assert event.id == "evt_55c8c149"

    def test_event_has_type(self, api):
        event = api.event("evt_55c8c149")
        assert event.type == "assign"

    def test_event_has_target_id(self, api):
        event = api.event("evt_55c8c149")
        assert event.target.id == "tea_55c8c149"

    def test_event_has_conversation_assignee(self, api):
        event = api.event("evt_55c8c149")
        assert event.conversation.assignee.id == "tea_55c8c149"

    def test_event_conversation_has_tags(self, api):
        event = api.event("evt_55c8c149")
        assert len(event.conversation.tags) == 1
        assert event.conversation.tags[0].id == "tag_55c8c149"

    def test_event_source_has_actions(self, api):
        event = api.event("evt_55c8c149")
        assert len(event.source.actions) == 1
        assert event.source.actions[0] == "Assign to Leela Turanga"
