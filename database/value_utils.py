from datetime import datetime
from decimal import Decimal


def clean(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value.lower() == "undefined":
        return None

    return value


def field(fields, index):

    if index >= len(fields):
        return None

    return clean(fields[index])


def numeric(value):

    value = clean(value)

    if value is None:
        return None

    try:
        return Decimal(value)

    except Exception:
        return None


def timestamp(value):

    value = clean(value)

    if value is None:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    except Exception:
        return None


def date_value(value):

    ts = timestamp(value)

    if ts is None:
        return None

    return ts.date()