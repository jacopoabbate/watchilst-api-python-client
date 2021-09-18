import pathlib
import json

import pytest
import requests

from watchlist_api_client import config_sender
from watchlist_api_client import data_structures


class TestValidateHeader:
    def test_validation_of_incorrectly_formatted_header(self):
        # Setup
        header_to_validate = "SourceID,RTSSymbol"
        # Exercise
        # Verify
        with pytest.raises(config_sender.ImproperFileFormat) as invalid_header_format:
            config_sender.validate_header(header_to_validate)
        assert str(invalid_header_format.value) == f"Improperly formatted header"
        # Cleanup - none

    def test_validation_of_correctly_formatted_header(self):
        # Setup
        header_to_validate = "sourceId,RTSsymbol"
        # Exercise
        # Verify
        assert config_sender.validate_header(header_to_validate) is None
        # Cleanup - none


class TestValidateRow:
    def test_validation_of_incorrectly_formatted_row(self):
        # Setup
        row_to_validate = "207, F:FDAX\\Z20"
        # Exercise
        # Verify
        with pytest.raises(config_sender.ImproperFileFormat) as invalid_config_file_format:
            config_sender.validate_row(row_to_validate, 1)
        assert str(invalid_config_file_format.value) == (
            f"Line 1 - Improperly formatted"
        )
        # Cleanup - none

    def test_validation_of_row_with_incorrect_symbol(self):
        # Setup
        row_to_validate = "207, F:FDAX??Z20"
        # Exercise
        # Verify
        with pytest.raises(config_sender.ImproperFileFormat) as invalid_config_file_format:
            config_sender.validate_row(row_to_validate, 1)
        assert str(invalid_config_file_format.value) == (
            f"Line 1 - Improperly formatted"
        )
        # Cleanup - none

    def test_validation_of_correctly_formatted_row(self):
        # Setup
        row_to_validate = "207,F:FDAX\\Z20"
        # Exercise
        # Verify
        assert config_sender.validate_row(row_to_validate, 1) is None
        # Cleanup - none


class TestValidateWatchlistConfigurationFile:
    def test_validation_of_correct_configuration_file(self):
        # Setup
        path_to_file = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data", "watchlist_config_20201118.csv"
        )
        # Exercise
        # Verify
        assert config_sender.validate_watchlist_configuration_file(path_to_file) is None
        # Cleanup - none

    def test_validation_of_file_with_incorrect_header(self):
        # Setup
        path_to_file = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data", "watchlist_config_wrong_header.csv"
        )
        # Exercise
        # Verify
        with pytest.raises(config_sender.ImproperFileFormat) as invalid_config_file_format:
            config_sender.validate_watchlist_configuration_file(path_to_file)
        assert str(invalid_config_file_format.value) == (
            f"Improperly formatted header"
        )
        # Cleanup - none

    def test_validation_of_file_with_incorrect_rows(self):
        # Setup
        path_to_file = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data", "watchlist_config_wrong_rows.csv"
        )
        # Exercise
        # Verify
        with pytest.raises(config_sender.ImproperFileFormat) as invalid_config_file_format:
            config_sender.validate_watchlist_configuration_file(path_to_file)
        assert str(invalid_config_file_format.value) == (
            f"Line 6 - Improperly formatted"
        )
        # Cleanup - none


class TestReactToStatusCode200:
    def test_reaction_to_status_code_200(self, mocked_successful_post_request):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        # Exercise
        with requests.post(url) as response:
            returned_config_summary = config_sender.react_to_status_code_200(response)
        # Verify
        expected_config_summary = data_structures.RequestSummary(
            submission_time="Wed, 18 Nov 2020 10:06:41 GMT",
            summary={
                "nbCreated": 0,
                "nbUpdated": 6,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": [],
                "updated": [
                    '207', '673', '676', '680', '684', '748'
                ],
                "failed": [],
                "deactivated": []
            },
        )
        assert returned_config_summary == expected_config_summary
        # Cleanup - none


class TestSendConfig:
    def test_successful_submission_of_config_file(self, mocked_successful_post_request):
        # Setup
        credentials = ("User", "Password")
        watchlist_endpoint = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        path_to_watchlist_config_file = (
            pathlib.Path(__file__).resolve().parent /
            "static_data" /
            "watchlist_config_20201118.csv"
        ).as_posix()
        # Exercise
        returned_config_summary = config_sender.send_config(
            watchlist_endpoint, credentials, path_to_watchlist_config_file,
        )
        # Verify
        expected_config_summary = data_structures.RequestSummary(
            submission_time="Wed, 18 Nov 2020 10:06:41 GMT",
            summary={
                "nbCreated": 0,
                "nbUpdated": 6,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": [],
                "updated": [
                    '207', '673', '676', '680', '684', '748'
                ],
                "failed": [],
                "deactivated": []
            },
        )
        assert returned_config_summary == expected_config_summary
        # Cleanup - none

    def test_unsuccessful_submission_of_configuration_file(self, mocked_500_status_code_request):
        # Setup
        credentials = ("User", "Password")
        watchlist_endpoint = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        path_to_watchlist_config_file = (
            pathlib.Path(__file__).resolve().parent /
            "static_data" /
            "watchlist_config_20201118.csv"
        ).as_posix()
        # Exercise
        # Verify
        expected_error_code = 500
        with pytest.raises(requests.exceptions.HTTPError) as error:
            config_sender.send_config(
                watchlist_endpoint, credentials, path_to_watchlist_config_file,
            )
        assert str(expected_error_code) in str(error.value)
        # Cleanup - none


class TestStringifyResponseSummary:
    def test_creation_of_summary_string_with_no_action(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 0,
                "nbUpdated": 0,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": [],
                "updated": [],
                "failed": [],
                "deactivated": []
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 0 new sources have been activated\n"
            f"  - 0 existing sources have been updated\n"
            f"  - 0 sources have failed\n"
            f"  - 0 existing sources have been "
            f"deactivated\n\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none

    def test_creation_of_summary_string_with_only_created_sources(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 2,
                "nbUpdated": 0,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": ['207', '673'],
                "updated": [],
                "failed": [],
                "deactivated": []
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 2 new sources have been activated\n"
            f"  - 0 existing sources have been updated\n"
            f"  - 0 sources have failed\n"
            f"  - 0 existing sources have been "
            f"deactivated\n\n"
            f"The following sources have been activated: 207, 673\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none

    def test_creation_of_summary_string_with_only_updated_sources(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 0,
                "nbUpdated": 2,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": [],
                "updated": ['207', '673'],
                "failed": [],
                "deactivated": []
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 0 new sources have been activated\n"
            f"  - 2 existing sources have been updated\n"
            f"  - 0 sources have failed\n"
            f"  - 0 existing sources have been "
            f"deactivated\n\n"
            f"The following sources have been updated: 207, 673\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none

    def test_creation_of_summary_string_with_only_failed_sources(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 0,
                "nbUpdated": 0,
                "nbFailed": 2,
                "nbDeactivated": 0,
                "created": [],
                "updated": [],
                "failed": ['596', '686'],
                "deactivated": []
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 0 new sources have been activated\n"
            f"  - 0 existing sources have been updated\n"
            f"  - 2 sources have failed\n"
            f"  - 0 existing sources have been "
            f"deactivated\n\n"
            f"The following sources have failed: 596, 686\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none

    def test_creation_of_summary_string_with_only_deactivated_sources(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 0,
                "nbUpdated": 0,
                "nbFailed": 0,
                "nbDeactivated": 2,
                "created": [],
                "updated": [],
                "failed": [],
                "deactivated": ['207', '673']
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 0 new sources have been activated\n"
            f"  - 0 existing sources have been updated\n"
            f"  - 0 sources have failed\n"
            f"  - 2 existing sources have been "
            f"deactivated\n\n"
            f"The following sources have been deactivated: 207, 673\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none

    def test_creation_of_summary_string_with_mix_of_actions_performed(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 2,
                "nbUpdated": 2,
                "nbFailed": 2,
                "nbDeactivated": 2,
                "created": ['676', '680'],
                "updated": ['207', '673'],
                "failed": ['596', '686'],
                "deactivated": ['684', '748']
            }
        )
        # Exercise
        generated_summary = config_sender.stringify_response_summary(request_summary)
        # Verify
        expected_summary = (
            f"Wed, 18 Nov 2020 10:06:41 GMT\n\n"
            f"Actions performed as a result of the request:\n"
            f"  - 2 new sources have been activated\n"
            f"  - 2 existing sources have been updated\n"
            f"  - 2 sources have failed\n"
            f"  - 2 existing sources have been "
            f"deactivated\n\n"
            f"The following sources have been activated: 676, 680\n"
            f"The following sources have been updated: 207, 673\n"
            f"The following sources have failed: 596, 686\n"
            f"The following sources have been deactivated: 684, 748\n"
        )
        assert generated_summary == expected_summary
        # Cleanup - none


class TestWriteRequestSummaryToJSON:
    def test_generation_of_correct_file_name(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 2,
                "nbUpdated": 2,
                "nbFailed": 2,
                "nbDeactivated": 2,
                "created": ['676', '680'],
                "updated": ['207', '673'],
                "failed": ['596', '686'],
                "deactivated": ['684', '748']
            }
        )
        path_to_parent_dir = pathlib.Path(__file__).resolve().parent / "static_data"
        # Exercise
        fpth = config_sender.write_request_summary_to_json(request_summary, path_to_parent_dir)
        # Verify
        assert fpth == path_to_parent_dir.joinpath(
            "request_summary_20201118T100641Z.json"
        ).as_posix()
        # Cleanup - none
        path_to_parent_dir.joinpath("request_summary_20201118T100641Z.json").unlink()

    def test_content_of_generated_json_file(self):
        # Setup
        request_summary = data_structures.RequestSummary(
            submission_time='Wed, 18 Nov 2020 10:06:41 GMT',
            summary={
                "nbCreated": 2,
                "nbUpdated": 2,
                "nbFailed": 2,
                "nbDeactivated": 2,
                "created": ['676', '680'],
                "updated": ['207', '673'],
                "failed": ['596', '686'],
                "deactivated": ['684', '748']
            }
        )
        path_to_parent_dir = pathlib.Path(__file__).resolve().parent / "static_data"
        # Exercise
        fpth = config_sender.write_request_summary_to_json(request_summary, path_to_parent_dir)
        # Verify
        with pathlib.Path(fpth).open(mode='rb') as infile:
            content = json.load(infile)
        assert content == request_summary.summary
        # Cleanup - none
        path_to_parent_dir.joinpath("request_summary_20201118T100641Z.json").unlink()
