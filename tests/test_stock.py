import pytest
from shoptrack.db import get_db

def get_auth_token(client):
    # Register and login
    client.post('/auth/register', 
                json={'username': 'stockuser', 'password': 'stockpass'})
    
    response = client.post('/auth/login', 
                          json={'username': 'stockuser', 'password': 'stockpass'})
    return response.get_json()['token']

def test_get_stock_with_auth(client):
    token = get_auth_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get('/stock/', headers=headers)
    assert response.status_code == 200

def test_create_product(client):
    token = get_auth_token(client)
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
    token = get_auth_token(client)
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
    token = get_auth_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # First create a product
    product_data = {
        'name': 'Stock Product',
        'stock': 10,
        'price': 19.99,
        'description': 'Product for stock testing'
    }
    client.post('/stock/', json=product_data, headers=headers)
    
    # Add stock
    stock_data = {'stock': 5}
    response = client.post('/stock/1/stock', 
                          json=stock_data, 
                          headers=headers)
    assert response.status_code == 200
    assert b'Stock added successfully' in response.data

def test_remove_stock(client):
    token = get_auth_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    # First create a product with stock
    product_data = {
        'name': 'Remove Stock Product',
        'stock': 10,
        'price': 19.99,
        'description': 'Product for stock removal testing'
    }
    client.post('/stock/', json=product_data, headers=headers)
    
    # Remove stock
    stock_data = {'stock': 3}
    response = client.delete('/stock/1/stock', 
                            json=stock_data, 
                            headers=headers)
    assert response.status_code == 200
    assert b'Stock removed successfully' in response.data
