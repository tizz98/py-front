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
