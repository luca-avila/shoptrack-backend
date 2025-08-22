from flask import jsonify, g, request
from shoptrack.db import get_db

def validate_product_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['name', 'stock', 'price']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate data types and ranges
    if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
        return False, "Name must be a non-empty string"
    
    if not isinstance(data['stock'], int) or data['stock'] < 0:
        return False, "Stock must be a non-negative integer"
    
    if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        return False, "Price must be a positive number"
    
    if 'description' in data and data['description'] is not None:
        if not isinstance(data['description'], str):
            return False, "Description must be a string"
    
    return True, None

def validate_product_ownership(product_id):
    db = get_db()
    product = db.execute(
        'SELECT * FROM product WHERE id = ? AND owner_id = ?', 
        (product_id, g.user_id)
    ).fetchone()
    
    if not product:
        return False, "Product not found or access denied"
    
    return True, product

def validate_stock_operation(product_id, quantity, operation='add'):
    is_valid, product = validate_product_ownership(product_id)
    if not is_valid:
        return False, product
    
    if not isinstance(quantity, int) or quantity <= 0:
        return False, "Quantity must be a positive integer"
    
    if operation == 'remove' and product['stock'] < quantity:
        return False, f"Insufficient stock. Available: {product['stock']}, requested: {quantity}"
    
    return True, product

def validate_json_request():
    if not request.is_json:
        return False, "Content-Type must be application/json"
    
    try:
        data = request.json
        if data is None:
            return False, "Invalid JSON data"
        return True, data
    except Exception:
        return False, "Invalid JSON format"

def validate_stock_data(data):
    if 'stock' not in data:
        return False, "Missing required field: stock"
    
    if not isinstance(data['stock'], int) or data['stock'] <= 0:
        return False, "Stock must be a positive integer"
    
    return True, None