import functools
import sqlite3
from datetime import datetime, timedelta
import secrets
import os

from flask import (
    Blueprint, g, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from shoptrack.db import get_db, get_placeholder, execute_query
from shoptrack.validation import validate_user_data, validate_json_request

# Import PostgreSQL error if available
try:
    import psycopg2
    from psycopg2 import IntegrityError as PostgresIntegrityError
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token and get user ID
        placeholder = get_placeholder()
        cursor = execute_query(f'SELECT user_id FROM sessions WHERE id = {placeholder}', (token,))
        session = cursor.fetchone()
        if not session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        g.user_id = session['user_id']
        
        return f(*args, **kwargs)
    return decorated_function

class Token:
    def __init__(self, token=None):
        self.token = token
    
    def verify(self):
        if not self.token:
            return False
        placeholder = get_placeholder()
        cursor = execute_query(f'SELECT * FROM sessions WHERE id = {placeholder}', (self.token,))
        session = cursor.fetchone()
        if session is None:
            return False
        if session['expires'] < datetime.now():
            # Clean up expired session
            execute_query(f'DELETE FROM sessions WHERE id = {placeholder}', (self.token,))
            get_db().commit()
            return False
        return True
    
    def generate(self):
        self.token = secrets.token_hex(32)
        return self.token



@bp.route('/register', methods=['POST'])
def register():
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    db = get_db()
    
    try:
        placeholder = get_placeholder()
        execute_query(
            f'INSERT INTO "user" (username, password) VALUES ({placeholder}, {placeholder})',
            (data['username'], generate_password_hash(data['password']))
        )
        get_db().commit()
    except (sqlite3.IntegrityError, PostgresIntegrityError) if POSTGRESQL_AVAILABLE else sqlite3.IntegrityError:
        error = f"User {data['username']} is already registered."
        return jsonify({'error': error}), 400
    
    return jsonify({'message': 'User registered successfully.'}), 201
    

@bp.route('/login', methods=['POST'])
def login():
    is_valid, result = validate_json_request()
    if not is_valid:
        return jsonify({'error': result}), 400
    
    data = result
    
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    placeholder = get_placeholder()
    cursor = execute_query(f'SELECT * FROM "user" WHERE LOWER(username) = LOWER({placeholder})', (data['username'],))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'error': 'Incorrect username.'}), 401
    
    if not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Incorrect password.'}), 401

    token = Token().generate()
    
    placeholder = get_placeholder()
    execute_query(
        f'INSERT INTO sessions (id, user_id, expires) VALUES ({placeholder}, {placeholder}, {placeholder})',
        (token, user['id'], datetime.now() + timedelta(days=30))
    )
    get_db().commit()
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username']
        }
    }), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    
    placeholder = get_placeholder()
    execute_query(f'DELETE FROM sessions WHERE id = {placeholder}', (token,))
    get_db().commit()
    return jsonify({'message': 'Logged out successfully.'}), 200