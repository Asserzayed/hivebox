import json
from config import API_VERSION

def test_version_endpoint(client):
    # Test the /version endpoint.
    response = client.get('/version')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == API_VERSION
