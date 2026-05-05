import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_report_page(client):
    response = client.get('/report')
    assert response.status_code == 200

def test_report_page_loads(client):
    response = client.get('/report')
    assert response.status_code == 200
