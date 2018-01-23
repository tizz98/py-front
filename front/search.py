from itertools import tee

from front.api import client


class ListSet:
    _pagination_key = '_pagination'
    _next_key = '_next'
    _results_key = '_results'

    def __init__(self, resource_cls):
        self._resource_cls = resource_cls
        self._results = self._results_generator()

    def __iter__(self):
        self._results, cpy = tee(self._results)
        return cpy

    def all(self):
        return self

    def _results_generator(self):
        response = client.get(self._resource_cls.Meta.list_path)

        if self._pagination_key in response:
            yield from self._paginate(response)
        else:
            yield from self._build_resources(response[self._results_key])

    def _paginate(self, response):
        next_page = response[self._pagination_key].get(self._next_key)

        if next_page is None:
            yield from self._build_resources(response[self._results_key])
        else:
            while next_page is not None:
                yield from self._build_resources(response[self._results_key])

                response = client.get(next_page)
                next_page = response[self._pagination_key].get(self._next_key)

    def _build_resources(self, rows):
        for row in rows:
            yield self._resource_cls.from_api_data(row)
