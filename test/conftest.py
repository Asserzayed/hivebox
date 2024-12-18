import pytest
from main import create_app
import responses  # for mocking HTTP requests
import re
from datetime import datetime, timezone



@pytest.fixture
def app():
    # Create and configure a new app instance for each test.
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    # A test client for the app.
    return app.test_client()

@pytest.fixture
def mock_temperature_api_success():
    # Mock the temperature API response.
    with responses.RequestsMock() as rsps:
        # Mock successful response
        pattern = re.compile(r"https://api\.opensensemap\.org/boxes/.*\?format=json")
        rsps.add(
            responses.GET,
            pattern,
            json={
                    "sensors": [
                        {
                            "unit": "°C",
                            "lastMeasurement": {
                                "value": "20.5",
                                "createdAt": datetime.now(timezone.utc).isoformat()
                            }
                        }
                    ]
                },
                status=200,
                match_querystring=True
        )
        yield rsps

@pytest.fixture
def mock_temperature_api_failure():
    # Mock the temperature API response.
    with responses.RequestsMock() as rsps:
        # Mock failed response
        pattern = re.compile(r"https://api\.opensensemap\.org/boxes/.*\?format=json")
        rsps.add(
            responses.GET,
            pattern,
            status=500
        )
        yield rsps
