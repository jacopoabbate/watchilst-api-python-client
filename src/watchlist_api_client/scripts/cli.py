"""
Module containing the command line app.
"""
import pathlib
import sys
from typing import Tuple

import click
import requests

from watchlist_api_client import config_retriever, config_sender, helpers


class MissingOnyxCredentialsError(Exception):
    """A class for an exception to raise in case of missing credentials."""


class InvalidOnyxCredentialTypeError(Exception):
    """A class for an exception to raise in case the credentials are not of the type string."""


def validate_credentials_type(credentials: Tuple[str, str]) -> None:
    if any(type(credential) is not str for credential in credentials):
        raise InvalidOnyxCredentialTypeError()


def validate_credentials_presence(credentials: Tuple[str, str]) -> None:
    """Checks for any missing credential.

    Parameters
    ----------
    credentials
    """
    username, password = credentials
    if all(credential is None for credential in credentials):
        raise MissingOnyxCredentialsError('Missing username and password')
    elif any(credential is None for credential in credentials):
        if username is None:
            raise MissingOnyxCredentialsError('Missing username')
        else:
            raise MissingOnyxCredentialsError('Missing password')


def validate_credentials(credentials: Tuple[str, str]) -> None:
    if not validate_credentials_presence(credentials):
        validate_credentials_type(credentials)


@click.group()
def watchlist():
    pass


@watchlist.command(name="submit")
@click.argument('config_file', type=click.Path(exists=True))
@click.option(
    '-u',
    '--user',
    type=click.STRING,
    envvar="ICE_API_USERNAME",
    help="The username used to access the Watchlist API.",
)
@click.option(
    '-p',
    '--password',
    type=click.STRING,
    envvar="ICE_API_PASSWORD",
    help="The password used to access the Watchlist API.",
)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    help=(
             "Do not display the summary of the actions resulting from submitting the "
             "request to the server."
    ),
)
@click.option(
    '--json',
    is_flag=True,
    help=(
        "Save the summary of the actions resulting from submitting the request to the server as "
        "as json."
    ),
)
@click.option(
    '-w',
    '--write-to',
    type=click.Path(exists=True),
    default=pathlib.Path().cwd().as_posix(),
    help=(
        "Specify the full path to the directory where the json summary will be written. "
        "To use in combination with the '--json' flag. If the '--json' flag is selected but "
        "no '--write-to' option is specified, the path will be set by default to the "
        "current working directory."
    ),
)
def send_config(config_file, user, password, quiet, json, write_to):
    """Submits a configuration file to the Watchlist API server.

    This commands accepts a path to a Watchlist API configuration file and, after
    verifying that the file is formatted according to its specifications, submits
    the configuration file to the Watchlist API server via a POST request. If the
    API call fails, an error is reported and the active configuration remains
    unchanged.

    If the API call is successful, the submit command returns a summary of all the
    actions that were performed as a result of the submission of the new configuration
    file (activation of new sources, update of existing sources, failed activation due
    to lack of entitlements, deactivation of existing sources) and an overview of which
    source IDs were affected.

    If you wish to have the summary returned in its native form, use the '--json' option.
    This will result in the raw request summary, which is returned by the Watchlist API
    server as a json object, being saved in its raw form in a json file.

    \b
    Positional arguments:
    \b
    CONFIG FILE          Full path to the Watchlist API configuration file location.
    """
    credentials = (user, password)
    try:
        validate_credentials(credentials)
    except MissingOnyxCredentialsError as missing_credentials_error:
        click.echo(f"Missing Credentials Error: {str(missing_credentials_error)}")
        sys.exit("Process finished with exit code 1")
    except InvalidOnyxCredentialTypeError:
        click.echo(f"Invalid credentials type")
        sys.exit("Process finished with exit code 1")

    try:
        config_sender.validate_watchlist_configuration_file(config_file)
    except config_sender.ImproperFileFormat as e:
        click.echo(f"Invalid Configuration File: {str(e)}")
        sys.exit("Process finished with exit code 1")

    watchlist_api_endpoint = (
        "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
    )
    known_error_causes = {
        "400": "Input CSV file is improperly formatted",
        "401": "Improper credentials",
        "500": "Failed request"
    }
    try:
        config_summary = config_sender.send_config(
            watchlist_api_endpoint,
            credentials,
            path_to_watchlist_config_file=config_file
        )
    except requests.exceptions.HTTPError as http_error:
        error_type = str(http_error).split(":")[0]
        error_code = error_type[:3]
        if error_code in known_error_causes.keys():
            click.echo(f"{error_type}: {known_error_causes.get(error_code)}")
        else:
            click.echo(f"{error_type}")
        sys.exit("Process finished with exit code 1")

    if not quiet:
        click.echo(config_sender.stringify_response_summary(config_summary))

    if json:
        path_to_request_summary = config_sender.write_request_summary_to_json(
            config_summary, write_to
        )
        click.echo(
            f"The summary of the actions performed as a result of the request has been written to: "
            f"\n"
            f"  {path_to_request_summary}"
        )
    sys.exit("Process finished with exit code 0")


@watchlist.command(name="retrieve")
@click.option(
    '-u',
    '--user',
    type=click.STRING,
    envvar="ICE_API_USERNAME",
    help="The username used to access the Watchlist API.",
)
@click.option(
    '-p',
    '--password',
    type=click.STRING,
    envvar="ICE_API_PASSWORD",
    help="The password used to access the Watchlist API.",
)
@click.option(
    '-t',
    '--timestamp',
    type=click.STRING,
    default=None,
    help=(
        "Specify a UTC timestamp formatted according to the ISO 8601 standard "
        "(YYYY-mm-ddTHH:MM:SSZ). The '--timestamp' option is used to retrieve the active "
        "configuration file at the point in time corresponding to the passed timestamp."
    ),
)
@click.option(
    '-w',
    '--write-to',
    type=click.Path(exists=True),
    default=pathlib.Path().cwd().as_posix(),
    help=(
        "Specify the full path to the directory where the retrieved configuration will be written. "
        "If no '--write-to' option is specified, the path will be set by default to the "
        "current working directory."
    ),
)
def get_config(user, password, timestamp, write_to):
    """Retrieves a Watchlist API configuration.

    This command allows the retrieval of both currently active and deactivated
    configurations. The type of configuration that is retrieved is controlled by the
    presence of the '--timestamp' option. If no '--timestamp' option is passed, the
    retrieve command will submit a GET request to retrieve the active configuration at
    the time of the API call. On the other hand, if the '--timestamp' option is used to
    specify a date and time in the UTC timezone, the retrieve command will submit a GET
    request to retrieve the configuration that was active at the time of the passed
    timestamp. If no active configuration is found, or if at the time of the passed
    timestamp no active configuration existed, an error is reported.
    """
    credentials = (user, password)
    try:
        validate_credentials(credentials)
    except MissingOnyxCredentialsError as missing_credentials_error:
        click.echo(f"Missing Credentials Error: {str(missing_credentials_error)}")
        sys.exit("Process finished with exit code 1")
    except InvalidOnyxCredentialTypeError:
        click.echo(f"Invalid credentials type")
        sys.exit("Process finished with exit code 1")

    watchlist_api_endpoint = (
        "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
    )
    if timestamp:
        watchlist_api_endpoint = helpers.join_base_url_and_query_string(
            watchlist_api_endpoint,
            helpers.prepare_timestamp_query_string(
                helpers.convert_raw_utc_timestamp_to_string(timestamp)
            )
        )

    known_error_causes = {
        "401": "Improper credentials",
        "404": "No active configuration for the given date and time",
    }
    try:
        retrieved_configuration = config_retriever.retrieve_config(
            watchlist_api_endpoint,
            credentials
        )
        file_path = config_retriever.retrieved_config_writer(retrieved_configuration, write_to)
        click.echo(
            f"The retrieved_configuration has been written to: "
            f"\n"
            f"  {file_path}"
        )
    except requests.exceptions.HTTPError as http_error:
        error_type = str(http_error).split(":")[0]
        error_code = error_type[:3]
        if error_code in known_error_causes.keys():
            click.echo(f"{error_type}: {known_error_causes.get(error_code)}")
        else:
            click.echo(f"{error_type}")
        sys.exit("Process finished with exit code 1")

    sys.exit("Process finished with exit code 0")


if __name__ == '__main__':
    watchlist()
