from datetime import datetime
from enum import Enum
from typing import NamedTuple, List, Union, Optional, Any
import urllib.parse

import requests

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

AnalyticsParameters = NamedTuple('AnalyticsParameters', (
    ('inbox_ids', Optional[List[str]]),
    ('tag_ids', Optional[List[str]]),
    ('start', datetime),
    ('end', datetime),
    ('timezone', Optional[str]),
    ('metrics', List[str]),
))


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

    def topic_conversations(
        self,
        topic_id: str,
        search: ConversationSearchParameters = None,
        options: RequestOptions = None,
    ):
        return self._get('topics/{id}/conversations'.format(id=topic_id), search=search, options=options)

    def conversations(self, search: ConversationSearchParameters = None, options: RequestOptions = None):
        return self._get('conversations', search=search, options=options)

    def conversation(self, conversation_id: str, options: RequestOptions = None):
        return self._get('conversations/{id}'.format(id=conversation_id), options=options)

    def download_attachment(self, attachment_url: str, download_path: str) -> None:
        options = RequestOptions(headers={'Content-Type': None, 'Accept': None})
        resp = self._raw_request('get', attachment_url, options=options)

        with open(download_path, 'wb+') as f:
            for chunk in resp.iter_content(chunk_size=128):
                f.write(chunk)

    def conversation_inboxes(self, conversation_id: str, options: RequestOptions = None):
        return self._get('conversations/{id}/inboxes'.format(id=conversation_id), options=options)

    def conversation_followers(self, conversation_id: str, options: RequestOptions = None):
        return self._get('conversations/{id}/followers'.format(id=conversation_id), options=options)

    def conversation_events(self, conversation_id: str, options: RequestOptions = None):
        return self._get('conversations/{id}/events'.format(id=conversation_id), options=options)

    def conversation_messages(self, conversation_id: str, options: RequestOptions = None):
        return self._get('conversations/{id}/messages'.format(id=conversation_id), options=options)

    def update_conversation(self, conversation_id: str, updates: dict, options: RequestOptions = None):
        return self._patch('conversations/{id}'.format(id=conversation_id), updates=updates, options=options)

    def analytics(self, params: AnalyticsParameters, team_id: Optional[str] = None, options: RequestOptions = None):
        endpoint = 'analytics'

        options = options or RequestOptions()
        add_parameters(params._asdict(), options)

        if team_id is not None:
            endpoint = 'teams/{id}/analytics'.format(id=team_id)

        return self._get(endpoint, options=options)

    def teammates(self, options: RequestOptions = None):
        return self._get('teammates', options=options)

    def teammate(self, teammate_id: str, options: RequestOptions = None):
        return self._get('teammates/{id}'.format(id=teammate_id), options=options)

    def _get(self, endpoint: str, search: EventSearchParameters = None, options: RequestOptions = None):
        return self._request_endpoint('get', endpoint, search=search, options=options)

    def _patch(self, endpoint: str, updates: dict, options: RequestOptions = None):
        options = options or RequestOptions()
        options.json = updates

        return self._request_endpoint('patch', endpoint, options=options)

    def _request_endpoint(
        self,
        method: str,
        endpoint: str,
        search: SearchParameters = None,
        options: RequestOptions = None,
    ) -> FrontObject:
        return self._request_url(method, urllib.parse.urljoin(self.base_url, endpoint), search=search, options=options)

    def _request_url(
        self,
        method: str,
        url: str,
        search: SearchParameters = None,
        options: RequestOptions = None,
    ) -> FrontObject:
        resp = self._raw_request(method, url, search=search, options=options)
        return FrontObject.from_bytes(resp.content, self)

    def _raw_request(
        self,
        method: str,
        url: str,
        search: SearchParameters = None,
        options: RequestOptions = None,
    ) -> requests.Response:
        options = options or RequestOptions()
        options.method = method
        options.url = url

        add_search_parameters(search, options)

        options.headers = (options.headers or {})
        options.headers.setdefault('Authorization', 'Bearer {}'.format(self._api_key))
        options.headers.setdefault('Content-Type', 'application/json')
        options.headers.setdefault('Accept', 'application/json')

        return self._requester.request(options)


def add_search_parameters(params: Optional[SearchParameters], options: RequestOptions) -> None:
    if params is not None:
        add_parameters({'q': params._asdict()}, options)


def add_parameters(params: Optional[dict], options: RequestOptions) -> None:
    if params is None:
        return

    for k, v in params.items():
        v = _front_parameter_value(v)

        if isinstance(v, list):
            for item in v:
                options.add_parameter('{}[]'.format(k), item)
            continue
        elif isinstance(v, dict):
            for vk, vv in v.items():
                key = '{}[{}]'.format(k, vk)
                if isinstance(vv, list):
                    key = key + '[]'
                elif vv is None:
                    continue
                options.add_parameter(key, vv)
            continue
        elif v is None:
            continue

        options.add_parameter(k, v)


def _front_parameter_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return timestamp(value)
    elif isinstance(value, Enum):
        return value.value
    elif isinstance(value, list):
        return list(map(_front_parameter_value, value))
    elif isinstance(value, dict):
        return {k: _front_parameter_value(v) for k, v in value.items()}
    return value
