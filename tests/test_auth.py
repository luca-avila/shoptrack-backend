import pytest
from shoptrack.db import get_db

def get_test_user_token(client):
    """Get token for the existing test user from data.sql."""
    response = client.post('/auth/login', 
                          json={'username': 'test', 'password': 'test'})
    return response.get_json()['token']

def test_register(client):
    response = client.post('/auth/register', 
                          json={'username': 'newuser', 'password': 'newpass'})
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_register_duplicate_username(client):
    # First registration
    client.post('/auth/register', 
                json={'username': 'duplicate', 'password': 'pass1'})
    
    # Second registration with same username
    response = client.post('/auth/register', 
                          json={'username': 'duplicate', 'password': 'pass2'})
    assert response.status_code == 400
    assert b'already registered' in response.data

def test_register_missing_fields(client):
    # Missing username
    response = client.post('/auth/register', 
                          json={'password': 'testpass'})
    assert response.status_code == 400
    assert b'Username is required' in response.data
    
    # Missing password
    response = client.post('/auth/register', 
                          json={'username': 'testuser'})
    assert response.status_code == 400
    assert b'Password is required' in response.data

def test_login_success(client):
    # Use existing test user
    response = client.post('/auth/login', 
                          json={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert b'Login successful' in response.data
    
    data = response.get_json()
    assert 'token' in data
    assert 'user' in data
    assert data['user']['username'] == 'test'

def test_login_invalid_credentials(client):
    response = client.post('/auth/login', 
                          json={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 401
    assert b'Incorrect username' in response.data

def test_login_missing_fields(client):
    # Missing username
    response = client.post('/auth/login', 
                          json={'password': 'testpass'})
    assert response.status_code == 400
    assert b'Username is required' in response.data
    
    # Missing password
    response = client.post('/auth/login', 
                          json={'username': 'testuser'})
    assert response.status_code == 400
    assert b'Password is required' in response.data

def test_protected_route_without_auth(client):
    response = client.get('/stock/')
    assert response.status_code == 401
    assert b'Invalid authorization header' in response.data

def test_protected_route_with_auth(client):
    # Use existing test user
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/stock/', headers=headers)
    assert response.status_code == 200  # Has test data
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_logout(client):
    token = get_test_user_token(client)
    
    # Logout
    response = client.post('/auth/logout', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data
    
    # Try to use the token after logout (should fail)
    response = client.get('/stock/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401

def test_invalid_token(client):
    response = client.get('/stock/', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert b'Unauthorized' in response.data