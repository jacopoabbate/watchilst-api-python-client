import pytest
import responses


@pytest.fixture
def mocked_response():
    """A pytest fixture to mock the behaviour of a server sending back a response."""
    with responses.RequestsMock() as mocked_response:
        yield mocked_response


@pytest.fixture
def mocked_successful_post_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
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
        status=200,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 10:06:41 GMT',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
            },
    )


@pytest.fixture
def mocked_400_status_code_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
            'type': '/errors/BadRequestError',
            'status': 400,
            'title': 'Input CSV file is improperly formatted',
        },
        status=400,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 15:10:34 GMT',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )


@pytest.fixture
def mocked_500_status_code_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
            "type": "/errors/NoSuchElementException",
            "status": 500,
        },
        status=500,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 15:23:52 GMT',
            'Content-Type': 'application/json;charset=UTF-8',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )


@pytest.fixture
def mocked_active_configuration_response(mocked_response):
    mocked_response.add(
        responses.GET,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        body=(
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
        status=200,
        content_type="'text/csv;charset=UTF-8'",
        headers={
            'Date': 'Fri, 20 Nov 2020 11:47:40 GMT',
            'Content-Length': '3311',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )


@pytest.fixture
def mocked_deactivated_configuration_response(mocked_response):
    mocked_response.add(
        responses.GET,
        url=(
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-18T12:30:52Z"
        ),
        body=(
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
        status=200,
        content_type="'text/csv;charset=UTF-8'",
        headers={
            'Date': 'Fri, 20 Nov 2020 13:05:56 GMT',
            'Content-Length': '223',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )


@pytest.fixture
def mocked_missing_configuration_response(mocked_response):
    mocked_response.add(
        responses.GET,
        url=(
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2019-11-18T12:30:52Z"
        ),
        body=b'',
        status=404,
        content_type="'text/csv;charset=UTF-8'",
        headers={
            'Date': 'Fri, 20 Nov 2020 14:05:55 GMT',
            'Content-Length': '0',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )
