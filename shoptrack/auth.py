import functools
import sqlite3
from datetime import datetime, timedelta
import secrets

from flask import (
    Blueprint, g, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from shoptrack.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

class Token:
    def __init__(self, token=None):
        self.token = token
    
    def verify(self):
        if not self.token:
            return False
        db = get_db()
        session = db.execute('SELECT * FROM sessions WHERE id = ?', (self.token,)).fetchone()
        if session is None:
            return False
        if session['expires'] < datetime.now():
            return False
        return True
    
    def generate(self):
        self.token = secrets.token_hex(32)
        return self.token



@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    error = None

    if not data.get('username'):
        error = 'Username is required.'
    elif not data.get('password'):
        error = 'Password is required.'

    if error is not None:
        return jsonify({'error': error}), 400
    
    try:
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (data['username'], generate_password_hash(data['password']))
        )
        db.commit()
    except sqlite3.IntegrityError:
        error = f"User {data['username']} is already registered."
        return jsonify({'error': error}), 400
    
    return jsonify({'message': 'User registered successfully.'}), 201
    

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    error = None

    if not data.get('username'):
        error = 'Username is required.'
    elif not data.get('password'):
        error = 'Password is required.'

    if error is not None:
        return jsonify({'error': error}), 400

    user = db.execute('SELECT * FROM user WHERE username = ?', (data['username'],)).fetchone()
    if user is None:
        return jsonify({'error': 'Incorrect username.'}), 401
    
    if not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Incorrect password.'}), 401

    token = Token().generate()
    
    db.execute(
        'INSERT INTO sessions (id, user_id, expires) VALUES (?, ?, ?)',
        (token, user['id'], datetime.now() + timedelta(days=30))
    )
    db.commit()
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username']
        }
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header'}), 401
    
    token = auth_header.split(' ')[1]
    
    if not Token(token).verify():
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    db.execute('DELETE FROM sessions WHERE id = ?', (token,))
    db.commit()
    return jsonify({'message': 'Logged out successfully.'}), 200
    
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        
        if not Token(token).verify():
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    return decorated_function