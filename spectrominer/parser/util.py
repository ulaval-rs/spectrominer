from datetime import datetime
from typing import Union

from pandas import Timestamp


def decode_date(date: Union[str, Timestamp]) -> datetime:
    if type(date) == Timestamp:
        return date.to_pydatetime()

    return datetime.strptime(date, '%m/%d/%Y %H:%M:%S')

