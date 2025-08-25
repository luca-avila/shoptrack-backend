import os
from flask import Blueprint, jsonify, request, g
from shoptrack.auth import login_required
from shoptrack.db import get_db, get_placeholder
from shoptrack.validation import (
    validate_product_data, 
    validate_product_ownership,
    validate_stock_operation, 
    validate_json_request,
    validate_stock_data
)

bp = Blueprint('stock', __name__)

@bp.route('/', methods=['GET'])
@login_required
def get_stock():
    db = get_db()
    placeholder = get_placeholder()
    products = db.execute(f'SELECT * FROM product WHERE owner_id = {placeholder} ORDER BY created DESC', (g.user_id,)).fetchall()

    if not products:
        return jsonify({'error': 'No products found'}), 404
    
    # Convert SQLite Row objects to dictionaries
    products_list = [dict(product) for product in products]
    return jsonify(products_list)

@bp.route('/<int:id>', methods=['GET'])
@login_required
def get_product(id):
    db = get_db()
    placeholder = get_placeholder()
    product = db.execute(f'SELECT * FROM product WHERE id = {placeholder} AND owner_id = {placeholder}', (id, g.user_id)).fetchone()

    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Convert SQLite Row object to dictionary
    return jsonify(dict(product))

@bp.route('/', methods=['POST'])
@login_required
def create_product():
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, error = validate_product_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    try:
        db = get_db()
        # Insert the product
        placeholder = get_placeholder()
        # Check if we're using PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # PostgreSQL - use RETURNING
            cursor = db.execute(
                f'INSERT INTO product (name, stock, price, description, owner_id) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}) RETURNING id',
                (data['name'], data['stock'], data['price'], data.get('description'), g.user_id)
            )
            product_id = cursor.fetchone()['id']
        else:
            # SQLite - use lastrowid
            cursor = db.execute(
                f'INSERT INTO product (name, stock, price, description, owner_id) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
                (data['name'], data['stock'], data['price'], data.get('description'), g.user_id)
            )
            product_id = cursor.lastrowid
        
        # Record initial stock as a 'buy' transaction if stock > 0
        if data['stock'] > 0:
            db.execute(
                f'INSERT INTO history (product_id, product_name, user_id, price, quantity, action) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
                (product_id, data['name'], g.user_id, data['price'], data['stock'], 'buy')
            )
        
        db.commit()
        return jsonify({'message': 'Product created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create product'}), 500

@bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, product = validate_product_ownership(id)
    if not is_valid:
        return jsonify({'error': product}), 404
    
    is_valid, error = validate_product_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    try:
        db = get_db()
        placeholder = get_placeholder()
        db.execute(
            f'UPDATE product SET name = {placeholder}, stock = {placeholder}, price = {placeholder}, description = {placeholder} WHERE id = {placeholder} AND owner_id = {placeholder}',
            (data['name'], data['stock'], data['price'], data.get('description'), id, g.user_id)
        )
        db.commit()
        return jsonify({'message': 'Product updated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update product'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id): 
    is_valid, product = validate_product_ownership(id)
    if not is_valid:
        return jsonify({'error': product}), 404
    
    try:
        db = get_db()
        placeholder = get_placeholder()
        db.execute(
            f'DELETE FROM product WHERE id = {placeholder} AND owner_id = {placeholder}',
            (id, g.user_id)
        )
        db.commit()
        return jsonify({'message': 'Product deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete product'}), 500

@bp.route('/<int:id>/stock', methods=['POST'])
@login_required
def add_stock(id):
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, error = validate_stock_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    is_valid, product = validate_stock_operation(id, data['stock'], 'add')
    if not is_valid:
        return jsonify({'error': product}), 400
    
    try:
        db = get_db()
        # Update stock
        placeholder = get_placeholder()
        db.execute(
            f'UPDATE product SET stock = stock + {placeholder} WHERE id = {placeholder} AND owner_id = {placeholder}',
            (data['stock'], id, g.user_id)
        )
        
        # Record 'buy' transaction in history
        db.execute(
            f'INSERT INTO history (product_id, product_name, user_id, price, quantity, action) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
            (id, product['name'], g.user_id, product['price'], data['stock'], 'buy')
        )
        
        db.commit()
        return jsonify({'message': 'Stock added successfully.'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to add stock'}), 500

@bp.route('/<int:id>/stock', methods=['DELETE'])
@login_required
def remove_stock(id):
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, error = validate_stock_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    is_valid, product = validate_stock_operation(id, data['stock'], 'remove')
    if not is_valid:
        return jsonify({'error': product}), 400
    
    try:
        db = get_db()
        # Update stock
        placeholder = get_placeholder()
        db.execute(
            f'UPDATE product SET stock = stock - {placeholder} WHERE id = {placeholder} AND owner_id = {placeholder}',
            (data['stock'], id, g.user_id)
        )
        
        # Record 'sell' transaction in history
        db.execute(
            f'INSERT INTO history (product_id, product_name, user_id, price, quantity, action) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})',
            (id, product['name'], g.user_id, product['price'], data['stock'], 'sell')
        )
        
        db.commit()
        return jsonify({'message': 'Stock removed successfully.'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to remove stock'}), 500

@bp.route('/history', methods=['GET'])
@login_required
def get_history():
    db = get_db()
    placeholder = get_placeholder()
    history = db.execute(f'''
        SELECT * FROM history 
        WHERE user_id = {placeholder} 
        ORDER BY created DESC
    ''', (g.user_id,)).fetchall()

    if not history:
        return jsonify({'error': 'No transaction history found'}), 404
    
    # Convert SQLite Row objects to dictionaries
    history_list = [dict(record) for record in history]
    return jsonify(history_list)

@bp.route('/<int:id>/history', methods=['GET'])
@login_required
def get_product_history(id):
    # Validate product ownership
    is_valid, product = validate_product_ownership(id)
    if not is_valid:
        return jsonify({'error': product}), 404
    
    db = get_db()
    placeholder = get_placeholder()
    history = db.execute(f'''
        SELECT * FROM history 
        WHERE product_id = {placeholder} AND user_id = {placeholder} 
        ORDER BY created DESC
    ''', (id, g.user_id)).fetchall()

    if not history:
        return jsonify({'error': 'No transaction history found for this product'}), 404
    
    # Convert SQLite Row objects to dictionaries
    history_list = [dict(record) for record in history]
    return jsonify(history_list)
