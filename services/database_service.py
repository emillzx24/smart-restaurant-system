# database_service.py
# Shared SQLite helpers for the Smart Restaurant System prototype.

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "restaurant.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SEED_PATH = BASE_DIR / "database" / "seed.sql"

VALID_ORDER_STATUSES = {
    "pending",
    "preparing",
    "ready",
    "completed",
    "cancelled",
}
VALID_PAYMENT_STATUSES = {"unpaid", "paid"}


def initialize_database() -> str:
    """Create and seed the local database the first time it is needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        return str(DB_PATH)

    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.executescript(SEED_PATH.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()

    return str(DB_PATH)


def get_connection() -> sqlite3.Connection:
    """Return a database connection with rows that can be accessed by column name."""
    initialize_database()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    """Validate a staff login against the users table."""
    user = _fetch_one(
        """
        SELECT
            user_id,
            username,
            password,
            role,
            is_active,
            created_at
        FROM users
        WHERE username = ?
        """,
        (username,),
    )

    if user is None:
        return None

    if not user["is_active"]:
        return None

    if user["password"] != password:
        return None

    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
    }

def get_menu_categories() -> list[dict[str, Any]]:
    """Return all menu categories in a simple list format for the UI."""
    return _fetch_all(
        """
        SELECT category_id, category_name, created_at
        FROM menu_categories
        ORDER BY category_name
        """
    )


def get_menu_items(
    category_id: int | None = None,
    available_only: bool = True,
) -> list[dict[str, Any]]:
    """Return menu items, with optional category and availability filters."""
    query = """
        SELECT
            m.item_id,
            m.category_id,
            c.category_name,
            m.item_name,
            m.description,
            m.price,
            m.is_available,
            m.created_at,
            m.updated_at
        FROM menu_items m
        JOIN menu_categories c ON c.category_id = m.category_id
        WHERE 1 = 1
    """
    parameters: list[Any] = []

    if category_id is not None:
        query += " AND m.category_id = ?"
        parameters.append(category_id)

    if available_only:
        query += " AND m.is_available = 1"

    query += " ORDER BY c.category_name, m.item_name"
    return _fetch_all(query, parameters)


def get_table_by_qr(qr_code_value: str) -> dict[str, Any] | None:
    """Look up a restaurant table using the QR value assigned to it."""
    return _fetch_one(
        """
        SELECT table_id, table_number, qr_code_value, status, created_at
        FROM restaurant_tables
        WHERE qr_code_value = ?
        """,
        (qr_code_value,),
    )


def create_order(
    table_id: int,
    items: list[dict[str, Any]],
    payment_status: str = "unpaid",
) -> dict[str, Any]:
    """Create an order and its line items in a single transaction."""
    _validate_payment_status(payment_status)

    if not items:
        raise ValueError("Order must include at least one item.")

    normalized_items = _normalize_items(items)
    connection = get_connection()

    try:
        table = connection.execute(
            """
            SELECT table_id, table_number, status
            FROM restaurant_tables
            WHERE table_id = ?
            """,
            (table_id,),
        ).fetchone()

        if table is None:
            raise ValueError("Table not found.")

        if table["status"] != "active":
            raise ValueError("Orders can only be created for active tables.")

        menu_items = _get_item_lookup(connection, [item["item_id"] for item in normalized_items])

        order_total = 0.0
        cursor = connection.execute(
            """
            INSERT INTO orders (table_id, order_status, payment_status, order_total)
            VALUES (?, 'pending', ?, 0)
            """,
            (table_id, payment_status),
        )
        order_id = cursor.lastrowid

        for item in normalized_items:
            menu_item = menu_items.get(item["item_id"])

            if menu_item is None:
                raise ValueError(f"Menu item {item['item_id']} was not found.")

            if not menu_item["is_available"]:
                raise ValueError(f"Menu item {menu_item['item_name']} is not available.")

            unit_price = float(menu_item["price"])
            subtotal = unit_price * item["quantity"]
            order_total += subtotal

            connection.execute(
                """
                INSERT INTO order_items (
                    order_id,
                    item_id,
                    quantity,
                    unit_price,
                    special_instructions,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    item["item_id"],
                    item["quantity"],
                    unit_price,
                    item["special_instructions"],
                    subtotal,
                ),
            )

        connection.execute(
            """
            UPDATE orders
            SET order_total = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
            """,
            (round(order_total, 2), order_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    order_details = get_order_details(order_id)
    if order_details is None:
        raise ValueError("Order was created but could not be reloaded.")
    return order_details


def get_orders(
    statuses: list[str] | tuple[str, ...] | None = None,
    table_id: int | None = None,
) -> list[dict[str, Any]]:
    """Return orders for staff views, with optional status or table filters."""
    query = """
        SELECT
            o.order_id,
            o.table_id,
            rt.table_number,
            o.order_status,
            o.payment_status,
            o.order_total,
            o.created_at,
            o.updated_at,
            o.completed_at,
            o.cancelled_at
        FROM orders o
        JOIN restaurant_tables rt ON rt.table_id = o.table_id
        WHERE 1 = 1
    """
    parameters: list[Any] = []

    if table_id is not None:
        query += " AND o.table_id = ?"
        parameters.append(table_id)

    if statuses:
        for status in statuses:
            _validate_order_status(status)
        placeholders = ", ".join("?" for _ in statuses)
        query += f" AND o.order_status IN ({placeholders})"
        parameters.extend(statuses)

    query += " ORDER BY o.created_at DESC, o.order_id DESC"
    return _fetch_all(query, parameters)


def get_order_details(order_id: int) -> dict[str, Any] | None:
    """Return one order with its table info and line items."""
    order = _fetch_one(
        """
        SELECT
            o.order_id,
            o.table_id,
            rt.table_number,
            o.order_status,
            o.payment_status,
            o.order_total,
            o.created_at,
            o.updated_at,
            o.completed_at,
            o.cancelled_at
        FROM orders o
        JOIN restaurant_tables rt ON rt.table_id = o.table_id
        WHERE o.order_id = ?
        """,
        (order_id,),
    )

    if order is None:
        return None

    order["items"] = _fetch_all(
        """
        SELECT
            oi.order_item_id,
            oi.order_id,
            oi.item_id,
            mi.item_name,
            oi.quantity,
            oi.unit_price,
            oi.special_instructions,
            oi.subtotal
        FROM order_items oi
        JOIN menu_items mi ON mi.item_id = oi.item_id
        WHERE oi.order_id = ?
        ORDER BY oi.order_item_id
        """,
        (order_id,),
    )
    return order


def update_order_status(order_id: int, new_status: str) -> dict[str, Any]:
    """Update the order workflow status and related timestamps."""
    _validate_order_status(new_status)
    _require_order(order_id)

    connection = get_connection()
    try:
        if new_status == "completed":
            connection.execute(
                """
                UPDATE orders
                SET
                    order_status = ?,
                    updated_at = CURRENT_TIMESTAMP,
                    completed_at = CURRENT_TIMESTAMP,
                    cancelled_at = NULL
                WHERE order_id = ?
                """,
                (new_status, order_id),
            )
        elif new_status == "cancelled":
            connection.execute(
                """
                UPDATE orders
                SET
                    order_status = ?,
                    updated_at = CURRENT_TIMESTAMP,
                    completed_at = NULL,
                    cancelled_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
                """,
                (new_status, order_id),
            )
        else:
            connection.execute(
                """
                UPDATE orders
                SET
                    order_status = ?,
                    updated_at = CURRENT_TIMESTAMP,
                    completed_at = NULL,
                    cancelled_at = NULL
                WHERE order_id = ?
                """,
                (new_status, order_id),
            )
        connection.commit()
    finally:
        connection.close()

    order_details = get_order_details(order_id)
    if order_details is None:
        raise ValueError("Order was updated but could not be reloaded.")
    return order_details


def update_payment_status(order_id: int, new_status: str) -> dict[str, Any]:
    """Update the payment status for an existing order."""
    _validate_payment_status(new_status)
    _require_order(order_id)

    connection = get_connection()
    try:
        connection.execute(
            """
            UPDATE orders
            SET payment_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
            """,
            (new_status, order_id),
        )
        connection.commit()
    finally:
        connection.close()

    order_details = get_order_details(order_id)
    if order_details is None:
        raise ValueError("Order was updated but could not be reloaded.")
    return order_details


def _fetch_all(query: str, parameters: list[Any] | tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Run a query and convert all returned rows into dictionaries."""
    connection = get_connection()
    try:
        rows = connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def _fetch_one(query: str, parameters: list[Any] | tuple[Any, ...] = ()) -> dict[str, Any] | None:
    """Run a query and return one row as a dictionary."""
    connection = get_connection()
    try:
        row = connection.execute(query, parameters).fetchone()
        return dict(row) if row is not None else None
    finally:
        connection.close()


def _get_item_lookup(connection: sqlite3.Connection, item_ids: list[int]) -> dict[int, dict[str, Any]]:
    """Load the menu items needed for order creation into a quick lookup map."""
    placeholders = ", ".join("?" for _ in item_ids)
    rows = connection.execute(
        f"""
        SELECT item_id, item_name, price, is_available
        FROM menu_items
        WHERE item_id IN ({placeholders})
        """,
        item_ids,
    ).fetchall()
    return {row["item_id"]: dict(row) for row in rows}


def _normalize_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate incoming order items before writing them to the database."""
    normalized_items: list[dict[str, Any]] = []

    for item in items:
        if "item_id" not in item:
            raise ValueError("Each order item must include an item_id.")
        if "quantity" not in item:
            raise ValueError("Each order item must include a quantity.")

        quantity = int(item["quantity"])
        if quantity <= 0:
            raise ValueError("Item quantity must be greater than 0.")

        normalized_items.append(
            {
                "item_id": int(item["item_id"]),
                "quantity": quantity,
                "special_instructions": item.get("special_instructions"),
            }
        )

    return normalized_items


def _require_order(order_id: int) -> None:
    """Fail fast when a requested order does not exist."""
    order = _fetch_one(
        """
        SELECT order_id
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,),
    )
    if order is None:
        raise ValueError("Order not found.")


def _validate_order_status(status: str) -> None:
    """Make sure only supported order statuses are used."""
    if status not in VALID_ORDER_STATUSES:
        raise ValueError(
            f"Invalid order status: {status}. "
            f"Expected one of: {', '.join(sorted(VALID_ORDER_STATUSES))}."
        )


def _validate_payment_status(status: str) -> None:
    """Make sure only supported payment statuses are used."""
    if status not in VALID_PAYMENT_STATUSES:
        raise ValueError(
            f"Invalid payment status: {status}. "
            f"Expected one of: {', '.join(sorted(VALID_PAYMENT_STATUSES))}."
        )
