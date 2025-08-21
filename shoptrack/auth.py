import functools
import sqlite3

from flask import (
    Blueprint, g, redirect, request, session, url_for, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from shoptrack.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    db = get_db()
    error = None

    if not data['username']:
        error = 'Username is required.'
    elif not data['password']:
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
    
    
