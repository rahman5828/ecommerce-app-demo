import pytest
import sys
import os

# Ensure root project directory is in sys.path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # now it will correctly find app.py


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test that the index route (/) returns HTTP 200."""
    res = client.get('/')
    assert res.status_code == 200


def test_api_products(client):
    """Test that /api/products returns a JSON list."""
    res = client.get('/api/products')
    assert res.status_code == 200
    assert res.is_json
    data = res.get_json()
    assert isinstance(data, list)

