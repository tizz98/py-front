import pytest

from front import Api

from . import get_jwt, RequesterMock


@pytest.fixture(scope='session', name='api')
def new_test_api() -> Api:
    api = Api(get_jwt())
    api._requester = RequesterMock()
    return api
