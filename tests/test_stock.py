import pytest
from shoptrack.db import get_db

def get_test_user_token(client):
    """Get token for the existing test user from data.sql."""
    response = client.post('/auth/login', 
                          json={'username': 'test', 'password': 'test'})
    return response.get_json()['token']

def test_get_stock_with_auth(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get('/stock/', headers=headers)
    # Should return 200 since there's test data
    assert response.status_code == 200
    # Check that we got a list of products
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_product(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    product_data = {
        'name': 'New Product',
        'stock': 5,
        'price': 29.99,
        'description': 'A new test product'
    }
    
    response = client.post('/stock/', 
                          json=product_data, 
                          headers=headers)
    assert response.status_code == 201
    assert b'Product created successfully' in response.data

def test_create_product_invalid_data(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # Missing required field
    product_data = {
        'name': 'New Product',
        'stock': 5
        # Missing price
    }
    
    response = client.post('/stock/', 
                          json=product_data, 
                          headers=headers)
    assert response.status_code == 400
    assert b'Missing required field' in response.data

def test_add_stock(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # Use existing test product (ID 1 from data.sql)
    stock_data = {'stock': 5}
    response = client.post('/stock/1/stock', 
                          json=stock_data, 
                          headers=headers)
    assert response.status_code == 200
    assert b'Stock added successfully' in response.data

def test_remove_stock(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # Use existing test product (ID 1 from data.sql)
    stock_data = {'stock': 3}
    response = client.delete('/stock/1/stock', 
                            json=stock_data, 
                            headers=headers)
    assert response.status_code == 200
    assert b'Stock removed successfully' in response.data

def test_get_history(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get('/stock/history', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Should have at least one history record from data.sql

def test_get_product_history(client):
    token = get_test_user_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # Use existing test product (ID 1 from data.sql)
    response = client.get('/stock/1/history', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Should have at least one history record for this product
