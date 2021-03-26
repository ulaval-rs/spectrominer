from datetime import datetime


def decode_date(date: str) -> datetime:
    return datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
