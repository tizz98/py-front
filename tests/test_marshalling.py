from datetime import datetime

import pytest
import pytz

from front.exceptions import InvalidTimezoneError
from front.marshalling import timestamp


class TestTimestamp:
    def test_conversion_is_accurate(self):
        assert timestamp(datetime(2016, 1, 25, 14, tzinfo=pytz.utc)) == 1453730400
        assert timestamp(datetime(2016, 1, 25, 6, tzinfo=pytz.timezone('America/Los_Angeles'))) == 1453729980

    def test_when_tz_is_not_provided_error_is_raised(self):
        with pytest.raises(InvalidTimezoneError):
            timestamp(datetime(2016, 1, 25, 14))
