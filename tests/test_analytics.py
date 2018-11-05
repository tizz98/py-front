from datetime import datetime
import urllib.parse

import pytz

from front import AnalyticsParameters


params = AnalyticsParameters(
    inbox_ids=['inb_55c8c149'],
    tag_ids=['tag_55c8c149'],
    start=datetime(2018, 1, 1, tzinfo=pytz.utc),
    end=datetime(2018, 2, 1, tzinfo=pytz.utc),
    timezone='utc',
    metrics=['avg_conversations_per_day', 'first_response_histo', 'first_response_graph'],
)

class TestAnalyticsRetrieval:
    def test_analytics_has_status(self, api):
        analytics = api.analytics(params)
        assert analytics.status == "pending"

    def test_analytics_has_progress(self, api):
        analytics = api.analytics(params)
        assert analytics.progress == 42

    def test_analytics_has_metrics(self, api):
        analytics = api.analytics(params)
        assert list(analytics.metrics)
        assert len(analytics.metrics) == 3
        assert analytics.metrics[0].t == "num"

    def test_parameters_are_properly_added(self, api):
        api.analytics(params)
        url = api._requester.calls[0].request.url

        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.unquote(parsed.query)

        expected_parts = sorted([
            "inbox_ids[]=inb_55c8c149",
            "tag_ids[]=tag_55c8c149",
            "start=1514764800.0",
            "end=1517443200.0",
            "timezone=utc",
            "metrics[]=avg_conversations_per_day",
            "metrics[]=first_response_histo",
            "metrics[]=first_response_graph",
        ])
        given_parts = sorted(query.split('&'))

        assert expected_parts == given_parts
