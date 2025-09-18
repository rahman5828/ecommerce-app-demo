import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200

def test_api_products(client):
    res = client.get('/api/products')
    assert res.is_json
    assert isinstance(res.get_json(), list)
