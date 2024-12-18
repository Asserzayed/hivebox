import pytest

# Test wrong endpoints
@pytest.mark.parametrize('endpoint', [
    '/nonexistent',
    '/version/',
    '/temperature/berlin'
])
def test_invalid_endpoints(client, endpoint):
    """Test invalid endpoints return 404."""
    response = client.get(endpoint)
    assert response.status_code == 404
