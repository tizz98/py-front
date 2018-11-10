class TestTagListing:
    def test_tag_has_id(self, api):
        tags = api.tags()
        assert tags[0].id == "tag_55c8c149"

    def test_tag_has_name(self, api):
        tags = api.tags()
        assert tags[0].name == "Robots"

    def test_tags_are_iterable(self, api):
        tags = api.tags()
        assert len(tags) == 1
        assert list(tags)


class TestTeammateTagListing:
    def test_tag_has_id(self, api):
        tags = api.teammate_tags("tea_55c8c149")
        assert tags[0].id == "tag_55c8c149"

    def test_tag_has_name(self, api):
        tags = api.teammate_tags("tea_55c8c149")
        assert tags[0].name == "Robots"

    def test_tags_are_iterable(self, api):
        tags = api.teammate_tags("tea_55c8c149")
        assert len(tags) == 1
        assert list(tags)


class TestTeamTagListing:
    def test_tag_has_id(self, api):
        tags = api.team_tags("tim_55c8c149")
        assert tags[0].id == "tag_55c8c149"

    def test_tag_has_name(self, api):
        tags = api.team_tags("tim_55c8c149")
        assert tags[0].name == "Robots"

    def test_tags_are_iterable(self, api):
        tags = api.team_tags("tim_55c8c149")
        assert len(tags) == 1
        assert list(tags)


class TestTagRetrieval:
    def test_tag_has_id(self, api):
        tag = api.tag("tag_55c8c149")
        assert tag.id == "tag_55c8c149"

    def test_tag_has_name(self, api):
        tag = api.tag("tag_55c8c149")
        assert tag.name == "Robots"


class TestTagCreation:
    pass


class TestTagDeletion:
    pass


class TestTagConversationListing:
    pass
