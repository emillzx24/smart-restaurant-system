# Database Teammate Guide

The goal is to make it easy for everyone to build their pages without needing to write a bunch of SQL.

## What I Set Up

I set up three main pieces:

1. The database structure
   - [`schema.sql`](./schema.sql)
2. Sample data for testing
   - [`seed.sql`](./seed.sql)
3. Shared Python helper functions
   - [`database_service.py`](../services/database_service.py)

The helper functions are the part most teammates will use.

## What This Means For You

If you are building a Streamlit page, you usually do not need to write SQL directly.

Instead, import the helper functions and use them to:
- load menu data
- find the table from a QR code
- create orders
- read orders for staff pages
- update order status
- update payment status

This keeps everyone using the same database logic.

## Quick Start

You can still build the database by hand with:

```bash
sqlite3 database/restaurant.db < database/schema.sql
sqlite3 database/restaurant.db < database/seed.sql
```

But the helper layer can also create the local database automatically the first time it is used.

So in most cases, you can just import a helper function and start building.

## Main Files To Know

- [`database/schema.sql`](./schema.sql)
  - the database structure
- [`database/seed.sql`](./seed.sql)
  - sample data for testing
- [`services/database_service.py`](../services/database_service.py)
  - shared Python functions for reading and writing data

## Database Tables

### `restaurant_tables`
This stores the restaurant tables.

Use this when you need:
- table number
- QR code value
- whether a table is active

### `menu_categories`
This stores menu sections like:
- Appetizers
- Main Courses
- Drinks

### `menu_items`
This stores the actual food and drink items.

Each item belongs to one category.

Examples:
- Classic Burger
- Fresh Lemonade
- Garden Salad

### `orders`
This stores the main order record.

It keeps things like:
- which table placed the order
- order status
- payment status
- total price

### `order_items`
This stores the individual items inside each order.

Example:
- one burger
- two lemonades
- special instructions

## Status Values To Use

Please use these exact words.

### Order status
- `pending`
- `preparing`
- `ready`
- `completed`
- `cancelled`

### Payment status
- `unpaid`
- `paid`

### Table status
- `active`
- `inactive`


## How To Import The Helper Functions

You can import directly like this:

```python
from services.database_service import get_menu_items, create_order, get_orders
```

Or like this:

```python
from services import get_menu_items, create_order, get_orders
```

## Main Functions And When To Use Them

### `initialize_database()`
What it does:
- creates the local database file if it does not exist yet
- runs the schema
- loads the sample data once

When to use it:
- mostly for setup
- usually the other helper functions call it for you

### `get_connection()`
What it does:
- opens a SQLite connection
- turns on foreign key rules

When to use it:
- only if you really need a custom query
- most teammates should not need this often

### `get_menu_categories()`
What it does:
- returns all menu categories as a list of dictionaries

When to use it:
- if you are building category tabs or sections on the customer menu page

Example:

```python
categories = get_menu_categories()
```

### `get_menu_items(category_id=None, available_only=True)`
What it does:
- returns menu items
- can return all items or only one category
- by default only returns available items

When to use it:
- customer menu page
- category filters
- showing only items that can currently be ordered

Examples:

```python
all_items = get_menu_items()
drinks = get_menu_items(category_id=3)
```

### `get_table_by_qr(qr_code_value)`
What it does:
- finds the table that matches a QR code value

When to use it:
- if the customer enters through a QR code
- if the app needs to know which table is placing the order

Example:

```python
table = get_table_by_qr("table-1-qr")
```

### `create_order(table_id, items, payment_status="unpaid")`
What it does:
- creates a full order
- saves the order itself
- saves all order items
- calculates subtotals and total for you

What it checks:
- table exists
- table is active
- item exists
- item is available
- quantity is valid
- payment status is valid

When to use it:
- when the customer clicks Place Order

Example:

```python
new_order = create_order(
    table_id=1,
    items=[
        {"item_id": 4, "quantity": 1, "special_instructions": "No onions"},
        {"item_id": 8, "quantity": 2},
    ],
)
```

Important:
- `items` should be a list
- each item should have at least `item_id` and `quantity`
- `special_instructions` is optional

### `get_orders(statuses=None, table_id=None)`
What it does:
- returns orders for staff pages
- can filter by status
- can filter by table

When to use it:
- cashier page
- kitchen page
- staff dashboard

Examples:

```python
all_orders = get_orders()
active_orders = get_orders(statuses=["pending", "preparing", "ready"])
table_two_orders = get_orders(table_id=2)
```

### `get_order_details(order_id)`
What it does:
- returns one full order
- includes the line items inside that order

When to use it:
- when staff clicks an order and wants to see item details

Example:

```python
order = get_order_details(1)
```

This is useful for showing:
- item names
- quantity
- instructions
- subtotal

### `update_order_status(order_id, new_status)`
What it does:
- updates the workflow status of an order
- also updates timestamps

When to use it:
- kitchen changes `pending` to `preparing`
- kitchen changes `preparing` to `ready`
- staff changes order to `completed`
- staff cancels an order

Example:

```python
updated_order = update_order_status(2, "ready")
```

### `update_payment_status(order_id, new_status)`
What it does:
- updates payment status

When to use it:
- cashier marks an order as paid

Example:

```python
updated_order = update_payment_status(2, "paid")
```

## What Different Teammates Will Probably Use

### If you are building the customer menu page
You will probably use:
- `get_menu_categories()`
- `get_menu_items()`

### If you are building the customer order page
You will probably use:
- `get_table_by_qr()`
- `create_order()`

### If you are building the staff dashboard
You will probably use:
- `get_orders()`
- `get_order_details()`
- `update_payment_status()`

### If you are building the kitchen page
You will probably use:
- `get_orders()`
- `get_order_details()`
- `update_order_status()`

## What The Functions Return

Most of the helper functions return normal Python dictionaries and lists.

That means you can do things like this:

```python
items = get_menu_items()

for item in items:
    print(item["item_name"], item["price"])
```

So you do not need to unpack raw SQL rows yourself.

## Helpful Example Workflows

### Example 1: Show the menu

```python
from services import get_menu_categories, get_menu_items

categories = get_menu_categories()
items = get_menu_items()
```

### Example 2: Place an order

```python
from services import create_order

order = create_order(
    table_id=1,
    items=[
        {"item_id": 1, "quantity": 1},
        {"item_id": 8, "quantity": 2, "special_instructions": "No ice"},
    ],
)
```

### Example 3: Show active staff orders

```python
from services import get_orders

orders = get_orders(statuses=["pending", "preparing", "ready"])
```

### Example 4: Mark an order ready

```python
from services import update_order_status

updated = update_order_status(order_id=3, new_status="ready")
```

## If You Need Something New

If your page needs a database action that is not covered yet, check first before adding custom SQL to the page file.

It is better to add a new shared helper function once than to have multiple pages all doing the same database logic differently.

## Short Version

If you are building a page and need data:
- use `get_menu_items()` for menu data
- use `create_order()` to place an order
- use `get_orders()` for staff and kitchen views
- use `get_order_details()` for one full order
- use `update_order_status()` for kitchen or workflow changes
- use `update_payment_status()` for cashier payment updates

That should cover most of the app for now.
