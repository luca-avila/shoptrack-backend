DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS sessions;

CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    price REAL NOT NULL CHECK (price > 0),
    description TEXT,
    owner_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    action TEXT NOT NULL CHECK (action IN ('buy', 'sell')),
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (product_id) REFERENCES product (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    expires TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);