import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_books_page(client):
    response = client.get('/books')
    assert response.status_code == 200

def test_add_book_requires_admin(client):
    response = client.get('/add_book')
    assert b"Access denied" in response.data

def test_add_and_search_book(client):
    # Try adding a book (without admin session, should deny)
    response = client.post('/add_book', data={
        'title': 'Integration Test Book',
        'author': 'Hamida',
        'year': '2026',
        'language': 'English'
    })
    assert b"Access denied" in response.data or response.status_code in (302, 403)

    # Search should still work
    response = client.get('/search_book?q=Integration')
    assert response.status_code == 200
def test_books_page_loads(client):
    response = client.get('/books')
    assert response.status_code == 200
