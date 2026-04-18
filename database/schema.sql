/*
schema.sql
Creates the initial SQLite schema for the Smart Restaurant System prototype.
*/

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

/* Table records used to identify restaurant tables and QR assignments. */
CREATE TABLE IF NOT EXISTS restaurant_tables (
    table_id INTEGER PRIMARY KEY,
    table_number INTEGER NOT NULL UNIQUE,
    qr_code_value TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* Categories keep the menu organized for both customers and staff. */
CREATE TABLE IF NOT EXISTS menu_categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* Menu items belong to a category and can be toggled on or off. */
CREATE TABLE IF NOT EXISTS menu_items (
    item_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK (price >= 0),
    is_available INTEGER NOT NULL DEFAULT 1
        CHECK (is_available IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES menu_categories(category_id)
);

/* Orders track the main order record for each table. */
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    table_id INTEGER NOT NULL,
    order_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (order_status IN ('pending', 'preparing', 'ready', 'completed', 'cancelled')),
    payment_status TEXT NOT NULL DEFAULT 'unpaid'
        CHECK (payment_status IN ('unpaid', 'paid')),
    order_total REAL NOT NULL DEFAULT 0 CHECK (order_total >= 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    cancelled_at TEXT,
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(table_id)
);

/* Order items store the individual menu items inside each order. */
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    special_instructions TEXT,
    subtotal REAL NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

/* Authorized Staff Accounts. */
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
        CHECK (role IN ('manager', 'kitchen')),
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* Indexes support the main lookups expected in the prototype. */
CREATE INDEX IF NOT EXISTS idx_menu_items_category_id
    ON menu_items(category_id);

CREATE INDEX IF NOT EXISTS idx_orders_table_id
    ON orders(table_id);

CREATE INDEX IF NOT EXISTS idx_orders_status
    ON orders(order_status);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id
    ON order_items(order_id);

COMMIT;
