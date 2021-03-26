from datetime import datetime

import pytest

from spectrominer.util import decode_date


@pytest.mark.parametrize('date, expected', [
    ('02/10/2021 20:08:03', datetime(year=2021, month=2, day=10, hour=20, minute=8, second=3)),
    ('02/11/2021 00:44:42', datetime(year=2021, month=2, day=11, hour=0, minute=44, second=42)),
])
def test_decode_date(date, expected):
    result = decode_date(date)

    assert result == expected
