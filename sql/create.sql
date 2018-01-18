CREATE TABLE IF NOT EXISTS Account (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    id SERIAL PRIMARY KEY,    
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL NOT NULL,
    stock_left INTEGER NOT NULL
);
