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

except ImportError as e:
    POSTGRESQL_AVAILABLE = False


def get_db():
    if 'db' not in g:
        # Check if we're in production (PostgreSQL)
        database_url = os.environ.get('DATABASE_URL')
        

        
        try:
            if database_url and POSTGRESQL_AVAILABLE:
                # PostgreSQL connection
                g.db = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
                g.is_postgresql = True
            else:
                # SQLite connection (development)
                g.db = sqlite3.connect(
                    current_app.config['DATABASE'],
                    detect_types=sqlite3.PARSE_DECLTYPES
                )
                g.db.row_factory = sqlite3.Row
                g.is_postgresql = False
        except Exception as e:
            raise
    return g.db

def execute_query(query, params=None):
    """Execute a query and return results, handling both SQLite and PostgreSQL"""
    db = get_db()
    
    if getattr(g, 'is_postgresql', False):
        # PostgreSQL - use cursor
        cursor = db.cursor()
        cursor.execute(query, params)
        return cursor
    else:
        # SQLite - execute directly on connection
        return db.execute(query, params)

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def convert_schema_for_postgresql(sql_script):
    """Convert SQLite schema to PostgreSQL syntax."""
    # Replace SQLite-specific syntax with PostgreSQL syntax
    sql_script = sql_script.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    sql_script = sql_script.replace('DEFAULT CURRENT_TIMESTAMP', 'DEFAULT NOW()')
    sql_script = sql_script.replace('REAL', 'DECIMAL(10,2)')
    sql_script = sql_script.replace('TEXT', 'VARCHAR(255)')
    
    # Quote reserved keywords - 'user' is a reserved keyword in PostgreSQL
    sql_script = sql_script.replace('DROP TABLE IF EXISTS user', 'DROP TABLE IF EXISTS "user"')
    sql_script = sql_script.replace('CREATE TABLE user', 'CREATE TABLE "user"')
    sql_script = sql_script.replace('REFERENCES user', 'REFERENCES "user"')
    
    return sql_script

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        sql_script = f.read().decode('utf8')
        
        # Check if we're using PostgreSQL
        if getattr(g, 'is_postgresql', False):  # PostgreSQL
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
        else:  # SQLite
            db.executescript(sql_script)

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def get_placeholder():
    """Get the correct placeholder for the current database."""
    database_url = os.environ.get('DATABASE_URL')
    return '%s' if database_url and POSTGRESQL_AVAILABLE else '?'

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
    # Register SQLite timestamp converter only if using SQLite
    if not os.environ.get('DATABASE_URL'):
        sqlite3.register_converter(
            'timestamp', lambda v: datetime.fromisoformat(v.decode())
        )