"""Implements the utilities needed to submit a configuration file to the Watchlist API."""
import csv
import json
import pathlib
import re
from typing import Tuple

import requests

from watchlist_api_client.data_structures import RequestSummary
from watchlist_api_client.helpers import convert_raw_utc_timestamp_to_string


class ImproperFileFormat(Exception):
    """An exception class that is raised when a Watchlist config file is improperly formatted."""

    pass


def validate_header(header: str) -> None:
    """Validates if the header of a Watchlist config file is properly formatted.

    Parameters
    ----------
    header: str
        The header of a Watchlist configuration file.

    Raises
    ------
    ImproperFileFormat
        The exception is accompanied by a message that informs that the header is not
        formatted accordingly to the specification.
    """
    header_pattern = r"^sourceId,RTSsymbol$"
    if not re.match(header_pattern, header):
        raise ImproperFileFormat("Improperly formatted header")


def validate_row(row: str, row_index: int) -> None:
    """Validates if a Watchlist configuration file's row is properly formatted.

    Using a regular expression, the function checks if the components in the passed row
    are in the correct order (first the source ID, followed by a comma, and the instrument
    symbol) and if the symbol is specified in a valid format (containing only the allowed
    characters for the definition of instruments symbols within the ICE Consolidated Feed
    data platform).

    Parameters
    ----------
    row: str
        A row of a Watchlist configuration file.
    row_index: str
        The index of the row passed as an input to the function.

    Raises
    ------
    ImproperFileFormat
        The exception is accompanied by a message informing that a row is not formatted
        accordingly to the specifications, together with the index of the row within the
        file.
    """
    row_pattern = r"^[0-9]{3,4},[A-Z0-9\\+;()!*\-.:/$@&_%#]+$"
    if not re.match(row_pattern, row):
        raise ImproperFileFormat(f"Line {row_index} - Improperly formatted")


def validate_watchlist_configuration_file(path_to_watchlist_config_file: str) -> None:
    """Checks if a Watchlist configuration file is properly formatted.

    Parameters
    ----------
    path_to_watchlist_config_file: str
        The location of the Watchlist configuration file to validate.

    Raises
    ------
    ImproperFileFormat
        If the passed file is not properly formatted, an ImproperFileFormat exception is
        raised, with attached a message that informs whether the file has an invalid
        formatting due to a mis-formatted header or due to a mis-formatted row.
    """
    with pathlib.Path(path_to_watchlist_config_file).open('r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(csv_reader):
            if index == 0:
                validate_header(','.join(row))
            else:
                validate_row(','.join(row), index)


def react_to_status_code_200(response: requests.Response) -> RequestSummary:
    """Embeds the submission time and the subscription summary in a ConfigSummary object.

    The function is designed to deal with the scenario of a successful request to update
    the configuration of the personal profile on the Watchlist API. In case of a
    successful submission of a new configuration file, in fact, the Watchlist API returns
    a JSON object that contains the summary of the actions performed as a result of the
    update request, stating the sources that were created, updated, duplicated, unchanged,
    failed and missing.

    The request summary, together with the timestamp of the response, are stored in a
    RequestSummary named-tuple and returned for further use.

    Parameters
    ----------
    response: requests.Response
        A Response object obtained by submitting a POST request to the Watchlist API.

    Returns
    -------
    RequestSummary
        A RequestSummary named-tuple containing the timestamp of the response and a
        dictionary that contains the summary of the action performed as a result of
        the request to update the configuration of the watchlist configuration file.
    """
    return RequestSummary(
        submission_time=response.headers.get('Date'),
        summary=response.json(),
    )


def send_config(
    watchlist_endpoint: str,
    credentials: Tuple[str, str],
    path_to_watchlist_config_file: str,
) -> RequestSummary:
    """Submits a Watchlist configuration file and returns the request summary.

    The function sends a POST request to the Watchlist API POST endpoint, with the new
    configuration file as a payload of the request. Depending on whether the request is
    successful or not, it returns a RequestSummary named-tuple containing the timestamp
    of the response and the request summary, or raises an HTTPError with the status code
    associated with the failed request.

    Parameters
    ----------
    watchlist_endpoint: str
        The POST endpoint of the Watchlist API.
    credentials: Tuple[str, str]
        A tuple containing the user name and password used to access the Watchlist API.
    path_to_watchlist_config_file
        The path to the location of the Watchlist configuration file that has to be
        uploaded.

    Returns
    -------
    RequestSummary
        A RequestSummary named-tuple containing the timestamp of the response and a
        dictionary that contains the summary of the action performed as a result of
        the request to update the configuration of the watchlist configuration file.

    Raises
    ------
    requests.exceptions.HTTPError
        In case the API call is not successful, returns an HTTPError with the status code
        and the type of error that occurred (whether the error was initiated on the client
        side or on the server side).

    """
    config_payload = {"file": pathlib.Path(path_to_watchlist_config_file).read_bytes()}
    with requests.post(watchlist_endpoint, auth=credentials, files=config_payload) as response:
        response.raise_for_status()
        return react_to_status_code_200(response)


def stringify_response_summary(request_summary: RequestSummary) -> str:
    """Converts a RequestSummary object in a human-readable string.

    Parameters
    ----------
    request_summary: RequestSummary
        A RequestSummary named tuple containing the timestamp associated with the API call
        that resulted in changes in the Watchlist configuration, and a dictionary that
        summarises the actions taken as a result of the request that uploaded the new
        configuration file.

    Returns
    -------
    str
        A representation of the content of the RequestSummary object in a human readable
        form.
    """
    summary = ""
    high_level_summary = (
        f"{request_summary.submission_time}\n\n"
        f"Actions performed as a result of the request:\n"
        f"  - {request_summary.summary.get('nbCreated')} new sources have been activated\n"
        f"  - {request_summary.summary.get('nbUpdated')} existing sources have been updated\n"
        f"  - {request_summary.summary.get('nbFailed')} sources have failed\n"
        f"  - {request_summary.summary.get('nbDeactivated')} existing sources have been deactivated"
        f"\n\n"
    )
    summary += high_level_summary
    if request_summary.summary.get('nbCreated') != 0:
        created_source_ids = (
            f"The following sources have been activated: "
            f"{', '.join(request_summary.summary.get('created'))}\n"
        )
        summary += created_source_ids
    if request_summary.summary.get('nbUpdated') != 0:
        updated_source_ids = (
            f"The following sources have been updated: "
            f"{', '.join(request_summary.summary.get('updated'))}\n"
        )
        summary += updated_source_ids
    if request_summary.summary.get('nbFailed') != 0:
        failed_source_ids = (
            f"The following sources have failed: "
            f"{', '.join(request_summary.summary.get('failed'))}\n"
        )
        summary += failed_source_ids
    if request_summary.summary.get('nbDeactivated') != 0:
        deactivated_source_ids = (
            f"The following sources have been deactivated: "
            f"{', '.join(request_summary.summary.get('deactivated'))}\n"
        )
        summary += deactivated_source_ids
    return summary


def write_request_summary_to_json(
    request_summary: RequestSummary,
    path_to_parent_dir: str,
) -> str:
    """Writes the request summary to a JSON file.

    Parameters
    ----------
    request_summary: RequestSummary
        A RequestSummary named-tuple containing the timestamp associated with the API call
        that resulted in changes in the Watchlist configuration, and a dictionary that
        summarises the actions taken as a result of the request that uploaded the new
        configuration file.
    path_to_parent_dir: str
        The path to the directory where the json file containing the request summary
        should be written to.

    Returns
    -------
    str
        The file path of the generated json file.

    """
    formatted_time = convert_raw_utc_timestamp_to_string(
        request_summary.submission_time,
        date_format="%Y%m%dT%H%M%SZ",
    )
    file_path = pathlib.Path(path_to_parent_dir).joinpath(f"request_summary_{formatted_time}.json")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('w') as outfile:
        json.dump(request_summary.summary, outfile, indent=2)
    return file_path.as_posix()
