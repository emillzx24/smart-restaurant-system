/*
seed.sql
Loads minimal demo data for local testing of the Smart Restaurant System schema.
*/

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

/* Demo table records used for local testing. */
INSERT INTO restaurant_tables (table_id, table_number, qr_code_value, status, created_at)
VALUES
    (1, 1, 'table-1-qr', 'active', '2026-04-02 10:00:00'),
    (2, 2, 'table-2-qr', 'active', '2026-04-02 10:00:00'),
    (3, 3, 'table-3-qr', 'active', '2026-04-02 10:00:00');

INSERT INTO menu_categories (category_id, category_name, created_at)
VALUES
    (1, 'Appetizers', '2026-04-02 10:05:00'),
    (2, 'Main Courses', '2026-04-02 10:05:00'),
    (3, 'Drinks', '2026-04-02 10:05:00');

/* Sample menu items that cover multiple categories. */
INSERT INTO menu_items (
    item_id,
    category_id,
    item_name,
    description,
    price,
    is_available,
    created_at,
    updated_at
)
VALUES
    (1, 1, 'Mozzarella Sticks', 'Crispy mozzarella sticks served with marinara.', 7.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (2, 1, 'Loaded Fries', 'Seasoned fries topped with cheese and bacon bits.', 8.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (3, 1, 'Garden Salad', 'Mixed greens with tomato, cucumber, and house dressing.', 6.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (4, 2, 'Classic Burger', 'Beef burger with lettuce, tomato, and house sauce.', 12.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (5, 2, 'Chicken Alfredo', 'Pasta tossed in Alfredo sauce with grilled chicken.', 14.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (6, 2, 'Veggie Wrap', 'Grilled vegetables with hummus in a warm wrap.', 10.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (7, 2, 'Fish Tacos', 'Three tacos with seasoned fish and slaw.', 13.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (8, 3, 'Fresh Lemonade', 'House-made lemonade served over ice.', 3.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (9, 3, 'Iced Tea', 'Unsweetened iced tea with lemon.', 3.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (10, 3, 'Sparkling Water', 'Chilled sparkling water.', 2.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00');

/* Orders show different states for testing the workflow. */
INSERT INTO orders (
    order_id,
    table_id,
    order_status,
    payment_status,
    order_total,
    created_at,
    updated_at,
    completed_at,
    cancelled_at
)
VALUES
    (1, 1, 'pending', 'unpaid', 14.50, '2026-04-02 11:00:00', '2026-04-02 11:00:00', NULL, NULL),
    (2, 2, 'preparing', 'paid', 17.50, '2026-04-02 11:05:00', '2026-04-02 11:15:00', NULL, NULL),
    (3, 3, 'ready', 'unpaid', 16.00, '2026-04-02 11:10:00', '2026-04-02 11:25:00', NULL, NULL);

/* Order items are kept separate so totals and joins can be tested. */
INSERT INTO order_items (
    order_item_id,
    order_id,
    item_id,
    quantity,
    unit_price,
    special_instructions,
    subtotal
)
VALUES
    (1, 1, 1, 1, 7.50, 'Extra marinara on the side.', 7.50),
    (2, 1, 8, 2, 3.50, 'No ice.', 7.00),
    (3, 2, 4, 1, 12.00, 'Cook medium well.', 12.00),
    (4, 2, 9, 1, 3.00, 'Add lemon.', 3.00),
    (5, 2, 10, 1, 2.50, NULL, 2.50),
    (6, 3, 6, 1, 10.00, 'Dressing on the side.', 10.00),
    (7, 3, 8, 1, 3.50, NULL, 3.50),
    (8, 3, 10, 1, 2.50, NULL, 2.50);

COMMIT;
