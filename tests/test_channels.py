class TestChannelListing:
    def test_channel_has_id(self, api):
        channels = api.channels()
        assert channels[0].id == "cha_55c8c149"

    def test_channel_has_address(self, api):
        channels = api.channels()
        assert channels[0].address == "team@planet-express.com"

    def test_channels_are_iterable(self, api):
        channels = api.channels()
        assert len(channels) == 1
        assert list(channels)


class TestTeammateChannelListing:
    def test_channel_has_id(self, api):
        channels = api.teammate_channels("tea_55c8c149")
        assert channels[0].id == "cha_55c8c149"

    def test_channel_has_address(self, api):
        channels = api.teammate_channels("tea_55c8c149")
        assert channels[0].address == "team@planet-express.com"

    def test_channels_are_iterable(self, api):
        channels = api.teammate_channels("tea_55c8c149")
        assert len(channels) == 1
        assert list(channels)


class TestTeamChannelListing:
    def test_channel_has_id(self, api):
        channels = api.team_channels("tim_55c8c149")
        assert channels[0].id == "cha_55c8c149"

    def test_channel_has_address(self, api):
        channels = api.team_channels("tim_55c8c149")
        assert channels[0].address == "team@planet-express.com"

    def test_channels_are_iterable(self, api):
        channels = api.team_channels("tim_55c8c149")
        assert len(channels) == 1
        assert list(channels)


class TestChannelRetrieval:
    def test_channel_has_id(self, api):
        channel = api.channel("cha_55c8c149")
        assert channel.id == "cha_55c8c149"

    def test_channel_has_address(self, api):
        channel = api.channel("cha_55c8c149")
        assert channel.address == "team@planet-express.com"

    def test_channel_has_type(self, api):
        channel = api.channel("cha_55c8c149")
        assert channel.type == "smtp"


class TestChannelUpdating:
    pass


class TestChannelCreation:
    pass
