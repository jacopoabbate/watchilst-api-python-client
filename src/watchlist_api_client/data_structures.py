"""Module containing user-defined data structures."""

from typing import Dict, List, NamedTuple, Union


class RequestSummary(NamedTuple):
    """Stores the content of the request summary obtained after submitting a new configuration."""

    submission_time: str
    summary: Dict[str, Union[int, List[str]]]


class RetrievedConfig(NamedTuple):
    """Stores the content of the configuration retrieved from the Watchlist API."""

    timestamp: str
    config_body: bytes
