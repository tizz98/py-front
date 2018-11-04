import urllib.parse
from datetime import datetime

import pytz

from front import RequestOptions
from front.api import ConversationSearchParameters, EventSearchParameters, Status, add_search_parameters


class TestAddSearchParameters:
    def test_lists_are_added_correctly_to_options(self):
        opts = RequestOptions()
        search = ConversationSearchParameters(statuses=[Status.ARCHIVED, Status.ASSIGNED])

        opts = add_search_parameters(search, opts)
        assert opts.params == {'q[statuses][]': ['archived', 'assigned']}

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

        opts = add_search_parameters(search, opts)
        assert opts.params == {'before': 1514764800}


class TestRequests:
    def test_headers_are_added(self, api):
        api.me()
        headers = api._requester.calls[0].request.headers

        assert headers['Authorization']
        assert headers['Content-Type']
        assert headers['Accept']
