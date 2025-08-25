import os
import sqlite3
from datetime import datetime

import click
from flask import current_app, g

# Add PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

def get_db():
    if 'db' not in g:
        # Check if we're in production (PostgreSQL)
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url and POSTGRESQL_AVAILABLE:
            # PostgreSQL connection
            g.db = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        else:
            # SQLite connection (development)
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def convert_schema_for_postgresql(sql_script):
    """Convert SQLite schema to PostgreSQL syntax."""
    # Replace SQLite-specific syntax with PostgreSQL syntax
    sql_script = sql_script.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    sql_script = sql_script.replace('DEFAULT CURRENT_TIMESTAMP', 'DEFAULT NOW()')
    return sql_script

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        sql_script = f.read().decode('utf8')
        
        # Check if we're using PostgreSQL
        if hasattr(db, 'execute'):  # SQLite
            db.executescript(sql_script)
        else:  # PostgreSQL
            # Convert schema for PostgreSQL
            sql_script = convert_schema_for_postgresql(sql_script)
            # Split SQL statements and execute one by one
            statements = sql_script.split(';')
            cursor = db.cursor()
            for statement in statements:
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
    # Register SQLite timestamp converter only if using SQLite
    if not os.environ.get('DATABASE_URL'):
        sqlite3.register_converter(
            'timestamp', lambda v: datetime.fromisoformat(v.decode())
        )