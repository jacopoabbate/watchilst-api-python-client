"""Implements helper function used across the watchlist_api_client library."""
import datetime
import urllib.parse

import dateutil.parser
import dateutil.tz


def parse_utc_timestamp(raw_timestamp: str) -> datetime.datetime:
    """Parses a UTC timestamp and returns the parsed date as a datetime object.

    Parameters
    ----------
    raw_timestamp: str
        A string containing a raw UTC timestamp. This can be anything from a date and
        time expressed according to the ISO 8601 standard (e.g. 2020-11-20T17:59:00Z) to
        a date and time expressed in a literal way (e.g. Fri, 20 November 2020 18:00:00
        UTC).

    Returns
    -------
    datetime.datetime
        A datetime object with the date and time parsed from the raw timestamp.
    """
    return dateutil.parser.parse(raw_timestamp).replace(tzinfo=dateutil.tz.tzutc())


def format_utc_timestamp(
    utc_timestamp: datetime.datetime,
    date_format: str = "%Y-%m-%dT%H:%M:%SZ",
) -> str:
    """Formats a datetime object according to a user defined date and time format.

    Parameters
    ----------
    utc_timestamp: datetime.datetime
        A datetime object containing the date and time components of a UTC timestamp.
    date_format: str
        A string controlling the output format. By default, date_format is set
        equal to the "%Y-%m-%dT%H:%M:%SZ" format string, which makes the function
        produce a date and time string formatted according to the ISO 8601 standard.

    Returns
    -------
    str
        The timestamp originally contained in the datetime object passed as an input to
        the function, formatted according to the date and time format expressed through
        the date_format parameter.

    References
    ----------
    For a complete list of formatting directives usable when defining the date_format
    parameter, see `strftime() and strptime() Behavior
    <https://docs.python.org/3.8/library/datetime.html#datetime.date.strftime>`_
    """
    return datetime.datetime.strftime(utc_timestamp, date_format)


def convert_raw_utc_timestamp_to_string(
    raw_timestamp: str,
    date_format: str = "%Y-%m-%dT%H:%M:%SZ",
) -> str:
    """Converts a raw UTC timestamp to a date and time string.

    Parameters
    ----------
    raw_timestamp: str
        A string containing a raw UTC timestamp. This can be anything from a date and
        time expressed according to the ISO 8601 standard (e.g. 2020-11-20T17:59:00Z) to
        a date and time expressed in a literal way (e.g. Fri, 20 November 2020 18:00:00
        UTC).
    date_format: str
        A string controlling the output format. By default, date_format is set equal to
        the "%Y-%m-%dT%H:%M:%SZ" format string, which makes the function produce a date
        and time string formatted according to the ISO 8601 standard.

    Returns
    -------
    str
        The raw timestamp passed as an input, converted into a date and time string
        according to the format specified by the date_format parameter.

    References
    ----------
    For a complete list of formatting directives usable when defining the date_format
    parameter, see `strftime() and strptime() Behavior
    <https://docs.python.org/3.8/library/datetime.html#datetime.date.strftime>`_
    """
    return format_utc_timestamp(parse_utc_timestamp(raw_timestamp), date_format)


def prepare_timestamp_query_string(iso_formatted_utc_timestamp: str) -> str:
    """Creates a dateTime query string from an ISO8601 formatted UTC timestamp string.

    Parameters
    ----------
    iso_formatted_utc_timestamp: str
        A string containing an ISO8601 formatted UTC time and date.

    Returns
    -------
    str
        A query string with the format dateTime=YYYY-mm-ddTHH-MM-SSZ.
    """
    return urllib.parse.urlencode(
        {"dateTime": iso_formatted_utc_timestamp},
    ).replace("%3A", ":")


def join_base_url_and_query_string(base_url: str, query_string: str) -> str:
    """Joins a base url and a query string.

    Parameters
    ----------
    base_url: str
        The base url to which the query string is to be attached.
    query_string: str
        A query string.

    Returns
    -------
    str
        The base url with attached the query string.
    """
    if base_url.endswith("/"):
        return f"{base_url[:-1]}?{query_string}"
    return f"{base_url}?{query_string}"
