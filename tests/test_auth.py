import pytest
from shoptrack.db import get_db

def test_register(client):
    response = client.post('/auth/register', 
                          json={'username': 'newuser', 'password': 'newpass'})
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(client):
    # Register a user first
    client.post('/auth/register', 
                json={'username': 'loginuser', 'password': 'loginpass'})
    
    # Login
    response = client.post('/auth/login', 
                          json={'username': 'loginuser', 'password': 'loginpass'})
    assert response.status_code == 200
    assert b'Login successful' in response.data
    
    # Check that we got a token
    data = response.get_json()
    assert 'token' in data

def test_login_wrong_password(client):
    response = client.post('/auth/login', 
                          json={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 401
    assert b'Incorrect username' in response.data

def test_protected_route_without_auth(client):
    response = client.get('/stock/')
    assert response.status_code == 401
    assert b'Invalid authorization header' in response.data

def test_protected_route_with_auth(client):
    # Register and login to get a token
    client.post('/auth/register', 
                json={'username': 'testuser', 'password': 'testpass'})
    
    login_response = client.post('/auth/login', 
                                json={'username': 'testuser', 'password': 'testpass'})
    token = login_response.get_json()['token']
    
    # Access protected route with token
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/stock/', headers=headers)
    assert response.status_code == 200  # Should work with test data