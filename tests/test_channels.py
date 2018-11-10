import json

from front.marshalling import detect_encoding


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
    def test_http_method_is_correct(self, api):
        api.update_channel("cha_55c8c149", updates={
            "settings": {
                "webhook_url": "https://example.io",
            },
        })

        req = api._requester.calls[0].request

        assert req.method == 'PATCH'

    def test_json_body_is_correct(self, api):
        api.update_channel("cha_55c8c149", updates={
            "settings": {
                "webhook_url": "https://example.io",
            },
        })

        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
            "settings": {
                "webhook_url": "https://example.io",
            },
        }


class TestChannelCreation:
    _data = {
        "type": "custom",
        "settings": {
            "webhook_url": "http://example.com",
        },
    }

    def test_http_method_is_correct(self, api):
        api.create_channel(self._data)
        req = api._requester.calls[0].request

        assert req.method == "POST"

    def test_json_body_is_correct(self, api):
        api.create_channel(self._data)
        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
            "type": "custom",
            "settings": {
                "webhook_url": "http://example.com",
            },
        }

    def test_response_has_id(self, api):
        channel = api.create_channel(self._data)
        assert channel.id == "cha_55c8c149"
