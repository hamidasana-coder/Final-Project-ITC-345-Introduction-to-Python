import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_borrow_requires_admin(client):
    response = client.get('/borrow_books/1')
    assert b"Access denied" in response.data or response.status_code in (302, 403)