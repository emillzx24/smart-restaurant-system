/*
seed.sql
Loads full menu demo data for local testing of the Smart Restaurant System schema.
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
    (2, 'Soups & Salads', '2026-04-02 10:05:00'),
    (3, 'Sushi Rolls', '2026-04-02 10:05:00'),
    (4, 'Nigiri', '2026-04-02 10:05:00'),
    (5, 'Bento Boxes', '2026-04-02 10:05:00'),
    (6, 'Kitchen Entrées', '2026-04-02 10:05:00'),
    (7, 'Noodles & Rice', '2026-04-02 10:05:00'),
    (8, 'Desserts', '2026-04-02 10:05:00'),
    (9, 'Drinks', '2026-04-02 10:05:00');

/* Full menu imported from Full menu - Sheet1.csv. */
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
    (1, 1, 'Edamame', 'Steamed soybeans with sea salt', 5.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (2, 1, 'Gyoza', 'Pan-fried pork dumplings', 7.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (3, 1, 'Karaage', 'Japanese fried chicken', 8.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (4, 1, 'Agedashi Tofu', 'Lightly fried tofu in broth', 7.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (5, 1, 'Shrimp Tempura', 'Lightly battered shrimp', 9.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (6, 2, 'Miso Soup', 'Soybean broth with tofu and scallions', 3.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (7, 2, 'House Salad', 'Greens with ginger dressing', 4.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (8, 2, 'Seaweed Salad', 'Seasoned seaweed salad', 6.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (9, 3, 'California Roll', 'Crab, avocado, cucumber', 7.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (10, 3, 'Spicy Tuna Roll', 'Tuna with spicy sauce', 8.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (11, 3, 'Salmon Avocado Roll', 'Salmon and avocado', 8.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (12, 3, 'Shrimp Tempura Roll', 'Shrimp tempura and cucumber', 9.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (13, 3, 'Philadelphia Roll', 'Salmon, cream cheese, avocado', 8.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (14, 4, 'Tuna Nigiri', '2 pieces', 7.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (15, 4, 'Salmon Nigiri', '2 pieces', 7.00, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (16, 4, 'Shrimp Nigiri', '2 pieces', 6.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (17, 4, 'Eel Nigiri', '2 pieces', 7.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (18, 5, 'Chicken Teriyaki Bento', 'Chicken teriyaki, rice, salad, gyoza', 15.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (19, 5, 'Beef Teriyaki Bento', 'Beef teriyaki, rice, salad, gyoza', 17.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (20, 5, 'Salmon Bento', 'Grilled salmon, rice, salad, gyoza', 17.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (21, 5, 'Tempura Bento', 'Shrimp tempura, rice, salad, gyoza', 16.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (22, 6, 'Chicken Teriyaki', 'Grilled chicken with teriyaki sauce and rice', 14.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (23, 6, 'Beef Teriyaki', 'Grilled beef with teriyaki sauce and rice', 17.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (24, 6, 'Salmon Teriyaki', 'Grilled salmon with teriyaki sauce and rice', 18.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (25, 6, 'Chicken Katsu', 'Breaded chicken cutlet with rice', 15.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (26, 6, 'Tonkatsu', 'Breaded pork cutlet with rice', 16.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (27, 7, 'Chicken Udon', 'Udon noodle soup with chicken', 14.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (28, 7, 'Beef Udon', 'Udon noodle soup with beef', 15.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (29, 7, 'Tonkotsu Ramen', 'Pork broth ramen', 15.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (30, 7, 'Chicken Fried Rice', 'Fried rice with chicken', 13.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (31, 7, 'Vegetable Fried Rice', 'Fried rice with vegetables', 12.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (32, 8, 'Mochi Ice Cream', 'Japanese ice cream dessert', 5.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (33, 8, 'Green Tea Ice Cream', 'Matcha ice cream', 4.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (34, 8, 'Tempura Cheesecake', 'Fried cheesecake', 6.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (35, 9, 'Green Tea', 'Hot green tea', 2.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (36, 9, 'Iced Green Tea', 'Cold green tea', 3.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (37, 9, 'Ramune', 'Japanese soda', 4.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (38, 9, 'Coke', 'Soft drink', 2.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (39, 9, 'Sprite', 'Soft drink', 2.95, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00'),
    (40, 9, 'Bottled Water', 'Water', 2.50, 1, '2026-04-02 10:10:00', '2026-04-02 10:10:00');

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
    (1, 1, 'pending', 'unpaid', 18.95, '2026-04-02 11:00:00', '2026-04-02 11:00:00', NULL, NULL),
    (2, 2, 'preparing', 'paid', 23.50, '2026-04-02 11:05:00', '2026-04-02 11:15:00', NULL, NULL),
    (3, 3, 'ready', 'unpaid', 18.50, '2026-04-02 11:10:00', '2026-04-02 11:25:00', NULL, NULL);

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
    (1, 1, 1, 1, 5.95, 'Light salt.', 5.95),
    (2, 1, 8, 2, 6.50, 'Extra sesame.', 13.00),
    (3, 2, 4, 1, 7.50, 'Sauce on the side.', 7.50),
    (4, 2, 9, 1, 7.50, 'No cucumber.', 7.50),
    (5, 2, 10, 1, 8.50, NULL, 8.50),
    (6, 3, 6, 1, 3.50, 'Extra scallions.', 3.50),
    (7, 3, 8, 1, 6.50, NULL, 6.50),
    (8, 3, 10, 1, 8.50, NULL, 8.50);

COMMIT;
