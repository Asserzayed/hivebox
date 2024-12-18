import json

def test_version_endpoint(client):
    # Test the /version endpoint.
    response = client.get('/version')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == '1.0.0'
