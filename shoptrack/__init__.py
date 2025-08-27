import os
import logging

from flask import Flask, jsonify
from flask_cors import CORS

def create_app(test_config = None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY', 'dev'),
        DATABASE = os.path.join(app.instance_path, 'shoptrack.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Debug psycopg2 availability
    try:
        import psycopg2
        app.logger.info("✅ psycopg2 import successful")
        app.logger.info(f"psycopg2 version: {psycopg2.__version__}")
    except ImportError as e:
        app.logger.error(f"❌ psycopg2 import failed: {e}")
    
    try:
        from psycopg2.extras import RealDictCursor
        app.logger.info("✅ RealDictCursor import successful")
    except ImportError as e:
        app.logger.error(f"❌ RealDictCursor import failed: {e}")

    @app.route('/hello')
    def hello():
        return 'Hello, World!'    

    # Add error handlers
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404

    from . import db
    db.init_app(app)
    CORS(app)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import stock
    app.register_blueprint(stock.bp, url_prefix='/stock')
    
    # Add a simple root endpoint
    @app.route('/')
    def index():
        return jsonify({'message': 'ShopTrack API is running'})

    return app