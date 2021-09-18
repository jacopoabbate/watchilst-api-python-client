import pytest

from watchlist_api_client.scripts import cli


class TestValidateCredentialsType:
    def test_validation_of_type_with_correct_credentials_tuple(self):
        # Setup
        credentials = ("Username", "Password")
        # Exercise
        # Verify
        assert cli.validate_credentials_type(credentials) is None
        # Cleanup - none

    def test_validation_of_type_with_tuple_with_one_wrong_credential(self):
        # Setup
        credentials = (12345, "Password")
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials_type(credentials)
        # Cleanup - none

    def test_validation_of_type_with_tuple_with_both_credentials_wrong(self):
        # Setup
        credentials = (12345, 6789)
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials_type(credentials)
        # Cleanup - none


class TestValidateCredentialsPresence:
    def test_complete_set_of_credentials_scenario(self):
        # Setup
        credentials = ("Username", "Password")
        # Exercise
        # Verify
        assert cli.validate_credentials_presence(credentials) is None
        # Cleanup - none

    def test_missing_username_scenario(self):
        # Setup
        credentials = (None, "Password")
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials_presence(credentials)
        assert str(missing_credentials_error.value) == "Missing username"
        # Cleanup - none

    def test_missing_password_scenario(self):
        # Setup
        credentials = ("Username", None)
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials_presence(credentials)
        assert str(missing_credentials_error.value) == "Missing password"
        # Cleanup - none

    def test_missing_credentials_scenario(self):
        # Setup
        credentials = (None, None)
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials_presence(credentials)
        assert str(missing_credentials_error.value) == "Missing username and password"
        # Cleanup - none


class TestValidateCredentials:
    def test_complete_set_of_correct_credentials_scenario(self):
        # Setup
        credentials = ("Username", "Password")
        # Exercise
        # Verify
        assert cli.validate_credentials(credentials) is None
        # Cleanup - none

    def test_complete_set_of_credentials_with_wrong_username_type_scenario(self):
        # Setup
        credentials = (12345, "Password")
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials(credentials)
        # Cleanup - none

    def test_complete_set_of_credentials_with_wrong_password_type_scenario(self):
        # Setup
        credentials = ("Username", 6789)
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials(credentials)
        # Cleanup - none

    def test_missing_username_scenario(self):
        # Setup
        credentials = (None, "Password")
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials(credentials)
        assert str(missing_credentials_error.value) == "Missing username"
        # Cleanup - none

    def test_missing_password_scenario(self):
        # Setup
        credentials = ("Username", None)
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials(credentials)
        assert str(missing_credentials_error.value) == "Missing password"
        # Cleanup - none

    def test_missing_credentials_scenario(self):
        # Setup
        credentials = (None, None)
        # Exercise
        # Verify
        with pytest.raises(cli.MissingOnyxCredentialsError) as missing_credentials_error:
            cli.validate_credentials(credentials)
        assert str(missing_credentials_error.value) == "Missing username and password"
        # Cleanup - none
