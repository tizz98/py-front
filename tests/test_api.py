import urllib.parse
from datetime import datetime

import pytz

from front import RequestOptions
from front.api import ConversationSearchParameters, EventSearchParameters, ContactSearchParameters, Status, add_search_parameters


class TestAddSearchParameters:
    def test_lists_are_added_correctly_to_request(self, api):
        search = ConversationSearchParameters(statuses=[Status.ARCHIVED, Status.ASSIGNED])
        api._request_endpoint('get', 'me', search=search)

        url = api._requester.calls[0].request.url
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.unquote(parsed.query)

        assert query == 'q[statuses][]=archived&q[statuses][]=assigned'

    def test_datetime_objects_are_properly_converted_to_unix_timestamps(self):
        opts = RequestOptions()
        search = EventSearchParameters(before=datetime(2018, 1, 1, tzinfo=pytz.utc), after=None, types=None)

        add_search_parameters(search, opts)
        assert opts.params == {'q[before]': 1514764800}

    def test_conversation_search_parameters(self):
        opts = RequestOptions()
        search = ConversationSearchParameters(statuses=[Status.ARCHIVED, Status.ASSIGNED])

        add_search_parameters(search, opts)
        assert opts.params == {'q[statuses][]': ['archived', 'assigned']}

    def test_event_search_parameters(self):
        opts = RequestOptions()
        search = EventSearchParameters(
            before=datetime(2018, 2, 1, tzinfo=pytz.utc),
            after=datetime(2018, 1, 1, tzinfo=pytz.utc),
            types=['foo', 'bar'],
        )

        add_search_parameters(search, opts)
        assert opts.params == {
            'q[before]': 1517443200,
            'q[after]': 1514764800,
            'q[types][]': ['foo', 'bar'],
        }

    def test_contact_search_parameters(self):
        opts = RequestOptions()
        search = ContactSearchParameters(
            updated_before=datetime(2018, 2, 1, tzinfo=pytz.utc),
            updated_after=datetime(2018, 1, 1, tzinfo=pytz.utc),
        )

        add_search_parameters(search, opts)
        assert opts.params == {
            'q[updated_before]': 1517443200,
            'q[updated_after]': 1514764800,
        }


class TestRequests:
    def test_headers_are_added(self, api):
        api.me()
        headers = api._requester.calls[0].request.headers

        assert headers['Authorization'].startswith('Bearer')
        assert headers['Content-Type'] == 'application/json'
        assert headers['Accept'] == 'application/json'
