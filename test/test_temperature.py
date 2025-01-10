import pytest
import json

@pytest.mark.usefixtures("mock_temperature_api_success")
def test_temperature_endpoint_success(client):
    # Test the /temperature endpoint with successful API response.
    response = client.get('/temperature')
    print(f"Test response data: {response.get_data(as_text=True)}")  # Debug print
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['Average temperature'] == '20.5'
    assert data['Status'] == 'Good'

@pytest.mark.usefixtures("mock_temperature_api_failure")
def test_temperature_endpoint_failure(client):
    # Test the /temperature endpoint with API failure.
    response = client.get('/temperature')
    print(f"Test response data: {response.get_data(as_text=True)}")  # Debug print
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data
