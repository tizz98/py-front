from datetime import datetime
from enum import Enum
from typing import NamedTuple, List, Union, Optional, Any
import urllib.parse

from .marshalling import FrontObject, timestamp
from .requests import RequestsRequester, RequestOptions


class Status(Enum):
    ASSIGNED = 'assigned'
    UNASSIGNED = 'unassigned'
    ARCHIVED = 'archived'
    DELETED = 'deleted'


ConversationSearchParameters = NamedTuple('SearchParameters', (
    ('statuses', Optional[List[Status]]),
))
EventSearchParameters = NamedTuple('EventSearchParameters', (
    ('types', Optional[List[str]]),
    ('before', Optional[datetime]),
    ('after', Optional[datetime]),
))
ContactSearchParameters = NamedTuple('ContactSearchParameters', (
    ('updated_before', Optional[datetime]),
    ('updated_after', Optional[datetime]),
))

SearchParameters = Union[ConversationSearchParameters, EventSearchParameters, ContactSearchParameters]


class Api:
    base_url = 'https://api2.frontapp.com'

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._requester = RequestsRequester()

    def me(self, options: RequestOptions = None):
        return self._get('me', options=options)

    def teams(self, options: RequestOptions = None):
        return self._get('teams', options=options)

    def team(self, team_id: str, options: RequestOptions = None):
        return self._get('teams/{id}'.format(id=team_id), options=options)

    def events(self, search: EventSearchParameters = None, options: RequestOptions = None):
        return self._get('events', search=search, options=options)

    def event(self, event_id: str, options: RequestOptions = None):
        return self._get('events/{id}'.format(id=event_id), options=options)

    def _get(self, endpoint: str, *, search: EventSearchParameters = None, options: RequestOptions = None):
        return self._request_endpoint('get', endpoint, search=search, options=options)

    def _request_endpoint(
        self,
        method: str,
        endpoint: str,
        *,
        search: SearchParameters = None,
        options: RequestOptions = None,
    ) -> FrontObject:
        return self._request_url(method, urllib.parse.urljoin(self.base_url, endpoint), search=search, options=options)

    def _request_url(
        self,
        method: str,
        url: str,
        *,
        search: SearchParameters = None,
        options: RequestOptions = None,
    ) -> FrontObject:
        options = options or RequestOptions()
        options.method = method
        options.url = url

        add_search_parameters(search, options)

        options.headers = (options.headers or {})
        options.headers.setdefault('Authorization', 'Bearer {}'.format(self._api_key))
        options.headers.setdefault('Content-Type', 'application/json')
        options.headers.setdefault('Accept', 'application/json')

        resp = self._requester.request(options)
        return FrontObject.from_bytes(resp.content, self)


def add_search_parameters(search: Optional[SearchParameters], options: RequestOptions) -> RequestOptions:
    if search is None:
        return options

    for k, v in search._asdict().items():
        v = _front_parameter_value(v)

        if isinstance(v, list):
            for item in v:
                options.add_parameter('q[{}][]'.format(k), item)
            continue
        elif v is None:
            continue

        options.add_parameter(k, v)

    return options


def _front_parameter_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return timestamp(value)
    elif isinstance(value, Enum):
        return value.value
    elif isinstance(value, list):
        return list(map(_front_parameter_value, value))
    return value
