import json
import os
from dotenv import load_dotenv

load_dotenv()
API_VERSION = os.getenv('API_VERSION', '0.0.0')

def test_version_endpoint(client):
    # Test the /version endpoint.
    response = client.get('/version')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == API_VERSION
