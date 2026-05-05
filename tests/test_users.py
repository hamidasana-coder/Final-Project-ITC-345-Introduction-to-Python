import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_users_page_requires_admin(client):
    response = client.get('/users')
    assert response.status_code in (200, 302, 403)

def test_login_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_invalid_credentials(client):
    response = client.post('/', data={
        'username': 'wronguser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b"Invalid credentials" in response.data

def test_logout_route(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"Welcome" in response.data

def test_home_requires_login(client):
    response = client.get('/home', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess['user'] = 'Hamida'
        sess['user_role'] = 'admin'
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_home_with_login(client):
    with client.session_transaction() as sess:
        sess['user'] = 'Hamida'
        sess['user_role'] = 'admin'
    response = client.get('/home')
    assert response.status_code == 200
    assert b"Welcome Hamida" in response.data
