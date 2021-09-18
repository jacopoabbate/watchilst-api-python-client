import pathlib

import pytest
import requests

from watchlist_api_client import config_retriever
from watchlist_api_client.data_structures import RetrievedConfig


class TestInferTimestampFromRetrievedResponse:
    def test_inference_of_timestamp_from_url_without_query_string(
        self,
        mocked_active_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        # Exercise
        with requests.get(url) as response:
            inferred_timestamp = config_retriever.infer_timestamp_from_retrieved_response(
                response,
            )
        # Verify
        expected_timestamp = "20201120T114740Z"
        assert inferred_timestamp == expected_timestamp
        # Cleanup - none

    def test_inference_of_timestamp_from_url_with_query_string(
        self,
        mocked_deactivated_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-18T12:30:52Z"
        )
        # Exercise
        with requests.get(url) as response:
            inferred_timestamp = config_retriever.infer_timestamp_from_retrieved_response(
                response,
            )
        # Verify
        expected_timestamp = "20201118T123052Z"
        assert inferred_timestamp == expected_timestamp
        # Cleanup - none


class TestPackageRetrievedConfiguration:
    def test_packaging_of_retrieved_active_configuration(
        self,
        mocked_active_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        # Exercise
        with requests.get(url) as response:
            packaged_active_configuration = config_retriever.package_retrieved_configuration(
                response,
            )
        # Verify
        expected_active_configuration = RetrievedConfig(
            timestamp="20201120T114740Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\H21\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\H21\n'
                b'207,F:FESX\\Z20\n'
                b'673,F2:ES\\H21\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\H21\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\H21\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\H21\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\H21\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\H21\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\H21\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\H21\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\H21\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\H21\n'
                b'748,F:FESX\\Z20\n'
            ),
        )
        assert packaged_active_configuration == expected_active_configuration
        # Cleanup - none

    def test_packaging_of_deactivated_configuration(
        self,
        mocked_deactivated_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-18T12:30:52Z"
        )
        # Exercise
        with requests.get(url) as response:
            packaged_deactivated_configuration = config_retriever.package_retrieved_configuration(
                response,
            )
        # Verify
        expected_deactivated_configuration = RetrievedConfig(
            timestamp="20201118T123052Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\Z20\n'
                b'207,F:FSMI\\Z20\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\Z20\n'
                b'748,F:FSMI\\Z20\n'
            ),
        )
        assert packaged_deactivated_configuration == expected_deactivated_configuration
        # Cleanup - none


class TestRetrieveConfig:
    def test_retrieval_of_missing_configuration(self, mocked_missing_configuration_response):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2019-11-18T12:30:52Z"
        )
        credentials = ("User", "Password")
        # Exercise
        # Verify
        with pytest.raises(requests.exceptions.HTTPError) as error:
            config_retriever.retrieve_config(url, credentials)
        assert str(404) in str(error.value)
        # Cleanup - none

    def test_retrieval_of_active_configuration(self, mocked_active_configuration_response):
        # Setup
        url = "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        credentials = ("User", "Password")
        # Exercise
        retrieved_configuration = config_retriever.retrieve_config(url, credentials)
        # Verify
        expected_configuration = RetrievedConfig(
            timestamp="20201120T114740Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\H21\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\H21\n'
                b'207,F:FESX\\Z20\n'
                b'673,F2:ES\\H21\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\H21\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\H21\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\H21\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\H21\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\H21\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\H21\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\H21\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\H21\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\H21\n'
                b'748,F:FESX\\Z20\n'
            ),
        )
        assert retrieved_configuration == expected_configuration
        # Cleanup - none

    def test_retrieval_of_deactivated_configuration(
        self, mocked_deactivated_configuration_response,
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-18T12:30:52Z"
        )
        credentials = ("User", "Password")
        # Exercise
        retrieved_configuration = config_retriever.retrieve_config(url, credentials)
        # Verify
        expected_configuration = RetrievedConfig(
            timestamp="20201118T123052Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\Z20\n'
                b'207,F:FSMI\\Z20\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\Z20\n'
                b'748,F:FSMI\\Z20\n'
            ),
        )
        assert retrieved_configuration == expected_configuration
        # Cleanup - none


class TestRetrievedConfigWriter:
    def test_correct_path_of_the_file(self):
        # Setup
        retrieved_config = RetrievedConfig(
            timestamp="20201118T123052Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\Z20\n'
                b'207,F:FSMI\\Z20\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\Z20\n'
                b'748,F:FSMI\\Z20\n'
            ),
        )
        path_to_directory = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data",
        ).as_posix()
        # Exercise
        path_to_file = config_retriever.retrieved_config_writer(retrieved_config, path_to_directory)
        # Verify
        expected_path_to_file = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data", "watchlist_config@20201118T123052Z.csv",
        ).as_posix()
        assert path_to_file == expected_path_to_file
        # Cleanup - none
        pathlib.Path(path_to_file).unlink()

    def test_correct_content_of_the_written_file(self):
        # Setup
        retrieved_config = RetrievedConfig(
            timestamp="20201118T123052Z",
            config_body=(
                b'sourceId,RTSsymbol\n'
                b'207,F:FDAX\\Z20\n'
                b'207,F:FESX\\Z20\n'
                b'207,F:FSMI\\Z20\n'
                b'673,F2:ES\\Z20\n'
                b'673,F2:NQ\\Z20\n'
                b'676,F2:RTY\\Z20\n'
                b'676,F2:SP\\Z20\n'
                b'680,F2:RTY\\Z20\n'
                b'680,F2:SP\\Z20\n'
                b'684,F2:ES\\Z20\n'
                b'684,F2:NQ\\Z20\n'
                b'748,F:FDAX\\Z20\n'
                b'748,F:FESX\\Z20\n'
                b'748,F:FSMI\\Z20\n'
            ),
        )
        path_to_directory = pathlib.Path(__file__).resolve().parent.joinpath(
            "static_data",
        ).as_posix()
        # Exercise
        path_to_file = config_retriever.retrieved_config_writer(retrieved_config, path_to_directory)
        # Verify
        assert pathlib.Path(path_to_file).read_bytes() == retrieved_config.config_body
        # Cleanup - none
        pathlib.Path(path_to_file).unlink()
