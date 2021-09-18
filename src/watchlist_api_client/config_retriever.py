"""Implements the utilities needed to retrieve the active configuration from the Watchlist API."""
import pathlib
from typing import Tuple
import urllib.parse

import requests

from watchlist_api_client.data_structures import RetrievedConfig
from watchlist_api_client.helpers import convert_raw_utc_timestamp_to_string


def infer_timestamp_from_retrieved_response(response: requests.Response) -> str:
    """Infers the timestamp of the retrieved response from the request URL.

    The function uses the fact that the retrieval of the active configuration is initiated
    by sending a GET request to the Watchlist API GET endpoint, without the specification
    of a dateTime query string. This signals to the function that the retrieved
    configuration is the active configuration at the time of the API call, and therefore
    returns as the timestamp associated with the retrieved configuration, the timestamp
    that is contained in the header of the response sent back by the Watchlist API.
    Conversely, when trying to retrieve a deactivated configuration, the GET request is
    sent to the Watchlist API GET endpoint with a specific dateTime query string, which
    specifies the point in time where we want to retrieve the at the time active
    configuration from. The returned deactivated configuration, will have a timestamp
    that is therefore equal to the passed dateTime query string, since the returned
    configuration is the one that was active at that specific point in time.

    Parameters
    ----------
    response: requests.Response
        A Response object that is returned as a result of the API call initiated to
        retrieve the active or a deactivated configuration.

    Returns
    -------
    str
        A string representing the timestamp of the retrieved configuration.
    """
    if urllib.parse.urlparse(response.request.url).query == '':
        return convert_raw_utc_timestamp_to_string(
            response.headers['Date'],
            date_format="%Y%m%dT%H%M%SZ",
        )
    else:
        return convert_raw_utc_timestamp_to_string(
            urllib.parse.urlparse(response.request.url).query.split("=")[1],
            date_format="%Y%m%dT%H%M%SZ",
        )


def package_retrieved_configuration(response: requests.Response) -> RetrievedConfig:
    """Packages the retrieved configuration in a RetrievedConfig named tuple.

    Parameters
    ----------
    response: requests.Response
        A Response object that is returned as a result of the API call initiated to
        retrieve the active or a deactivated configuration.

    Returns
    -------
    RetrievedConfig
        A named tuple containing the timestamp of the retrieved configuration, and a
        byte-string object containing the body of the retrieved configuration.
    """
    return RetrievedConfig(
        timestamp=infer_timestamp_from_retrieved_response(response),
        config_body=response.content,
    )


def retrieve_config(
    watchlist_endpoint: str,
    credentials: Tuple[str, str],
) -> RetrievedConfig:
    """Retrieves an active or deactivated configuration from the Watchlist API.

    Parameters
    ----------
    watchlist_endpoint: str
        The watchlist API GET endpoint.
    credentials: Tuple[str, str]
        A tuple containing the username and password used to access the Watchlist API.

    Returns
    -------
    RetrievedConfig
        A named tuple containing the timestamp of the retrieved configuration, and a
        byte-string object containing the body of the retrieved configuration.
    """
    with requests.get(watchlist_endpoint, auth=credentials) as response:
        response.raise_for_status()
        return package_retrieved_configuration(response)


def retrieved_config_writer(retrieved_config: RetrievedConfig, path_to_directory: str) -> str:
    """Writes the content of a RetrievedConfig named tuple to a csv file.

    Parameters
    ----------
    retrieved_config: RetrievedConfig
        A named tuple containing the timestamp of the retrieved configuration, and a
        byte-string object containing the body of the retrieved configuration.
    path_to_directory: str
        The path to the directory where the csv file containing the retrieved
        configuration will be written.

    Returns
    -------
    str
        The file path of the csv file containing the retrieved configuration.
    """
    file_path = pathlib.Path(path_to_directory).joinpath(
        f"watchlist_config@{retrieved_config.timestamp}.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with pathlib.Path(file_path).open('wb') as outfile:
        outfile.write(retrieved_config.config_body)
    return file_path.as_posix()
