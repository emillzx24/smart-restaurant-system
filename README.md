# Smart Restaurant System

## Overview
Prototype web application that allows customers to place orders digitally and enables staff to manage and track those orders.

This branch currently focuses on the initial database setup for the project.

## Tech Stack
- Python
- Streamlit
- SQLite

## Project Structure
- app.py
- pages/
- components/
- services/
  - database_service.py
- database/
  - schema.sql
  - seed.sql
- models/

## Setup
1. Install Streamlit:
   `pip install streamlit`
2. Create the local SQLite database from the schema:
   `sqlite3 database/restaurant.db < database/schema.sql`
3. Load demo seed data:
   `sqlite3 database/restaurant.db < database/seed.sql`
4. Run the app:
   `streamlit run app.py`

## Shared Database Helpers
The project now includes a shared helper layer in `services/database_service.py` so teammates do not need to write SQL directly for common tasks.

Example import:
`from services.database_service import get_menu_items, create_order, get_orders`

Main helper functions:
- `initialize_database()` creates and seeds the local database if it does not already exist.
- `get_connection()` returns a SQLite connection with foreign keys enabled.
- `get_menu_categories()` returns all menu categories.
- `get_menu_items(category_id=None, available_only=True)` returns menu items as a list of dictionaries.
- `get_table_by_qr(qr_code_value)` finds a table using its QR code value.
- `create_order(table_id, items, payment_status='unpaid')` creates an order and its order items in one transaction.
- `get_orders(statuses=None, table_id=None)` returns orders for staff views.
- `get_order_details(order_id)` returns one order plus its line items.
- `update_order_status(order_id, new_status)` updates the order workflow status.
- `update_payment_status(order_id, new_status)` updates the payment status.

Example order payload for `create_order()`:
```python
items = [
    {"item_id": 4, "quantity": 1, "special_instructions": "No onions"},
    {"item_id": 8, "quantity": 2},
]
```

The helper layer automatically creates `database/restaurant.db` from `schema.sql` and `seed.sql` the first time it is used, so teammates can build pages without doing the setup by hand every time.

## Database Notes
- The main database files for this phase are `database/schema.sql` and `database/seed.sql`.
- The generated `database/restaurant.db` file is for local testing and should not be treated as source code.
- The schema includes the core project tables: restaurant tables, menu categories, menu items, orders, and order items.

## Core Functionality
- Customer order input (in progress)
- Staff order management (planned)
- Order storage and status tracking (database setup complete for initial prototype)

## Team
- Stephanie Dunlap  
- Geraldine Osawemen  
- Andrei Fajutagana  
- Emilio Laboy  
