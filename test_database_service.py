# test_database_service.py
# Verifies SQLite helper behavior against the seeded restaurant database.

import importlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


database_service = importlib.import_module("services.database_service")


class DatabaseServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="smart_restaurant_tests_"))
        cls.db_dir = cls.temp_dir / "database"
        cls.db_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy(REPO_ROOT / "database" / "schema.sql", cls.db_dir / "schema.sql")
        shutil.copy(REPO_ROOT / "database" / "seed.sql", cls.db_dir / "seed.sql")

        cls.original_db_path = database_service.DB_PATH
        cls.original_schema_path = database_service.SCHEMA_PATH
        cls.original_seed_path = database_service.SEED_PATH

        database_service.DB_PATH = cls.db_dir / "restaurant_test.db"
        database_service.SCHEMA_PATH = cls.db_dir / "schema.sql"
        database_service.SEED_PATH = cls.db_dir / "seed.sql"
        database_service.initialize_database()

    @classmethod
    def tearDownClass(cls):
        database_service.DB_PATH = cls.original_db_path
        database_service.SCHEMA_PATH = cls.original_schema_path
        database_service.SEED_PATH = cls.original_seed_path
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_initialize_database_creates_seeded_tables(self):
        self.assertTrue(database_service.DB_PATH.exists())
        categories = database_service.get_menu_categories()
        self.assertEqual(9, len(categories))
        self.assertEqual("Appetizers", categories[0]["category_name"])

    def test_get_menu_items_can_filter_by_category(self):
        drinks = database_service.get_menu_items(category_id=9)
        self.assertEqual(6, len(drinks))
        self.assertTrue(all(item["category_name"] == "Drinks" for item in drinks))

    def test_get_table_by_qr_returns_expected_table(self):
        table = database_service.get_table_by_qr("table-2-qr")
        self.assertIsNotNone(table)
        self.assertEqual(2, table["table_number"])
        self.assertEqual("active", table["status"])

    def test_create_order_calculates_total_and_preserves_instructions(self):
        order = database_service.create_order(
            table_id=1,
            items=[
                {"item_id": 18, "quantity": 1, "special_instructions": "No onions"},
                {"item_id": 35, "quantity": 2},
            ],
        )
        self.assertEqual("pending", order["order_status"])
        self.assertEqual("unpaid", order["payment_status"])
        self.assertAlmostEqual(21.85, order["order_total"], places=2)
        self.assertEqual(2, len(order["items"]))
        self.assertEqual("No onions", order["items"][0]["special_instructions"])

    def test_create_order_rejects_empty_item_list(self):
        with self.assertRaisesRegex(ValueError, "Order must include at least one item"):
            database_service.create_order(table_id=1, items=[])

    def test_create_order_rejects_invalid_payment_status(self):
        with self.assertRaisesRegex(ValueError, "Invalid payment status"):
            database_service.create_order(
                table_id=1,
                items=[{"item_id": 1, "quantity": 1}],
                payment_status="partial",
            )

    def test_create_order_rejects_inactive_table(self):
        connection = database_service.get_connection()
        try:
            connection.execute(
                "UPDATE restaurant_tables SET status = 'inactive' WHERE table_id = 3"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(ValueError, "active tables"):
            database_service.create_order(table_id=3, items=[{"item_id": 1, "quantity": 1}])

        connection = database_service.get_connection()
        try:
            connection.execute(
                "UPDATE restaurant_tables SET status = 'active' WHERE table_id = 3"
            )
            connection.commit()
        finally:
            connection.close()

    def test_update_order_status_completed_sets_completed_timestamp(self):
        order = database_service.update_order_status(1, "completed")
        self.assertEqual("completed", order["order_status"])
        self.assertIsNotNone(order["completed_at"])
        self.assertIsNone(order["cancelled_at"])

    def test_update_order_status_cancelled_sets_cancelled_timestamp(self):
        order = database_service.update_order_status(2, "cancelled")
        self.assertEqual("cancelled", order["order_status"])
        self.assertIsNone(order["completed_at"])
        self.assertIsNotNone(order["cancelled_at"])

    def test_update_payment_status_marks_order_paid(self):
        order = database_service.update_payment_status(3, "paid")
        self.assertEqual("paid", order["payment_status"])

    def test_get_orders_can_filter_by_status(self):
        pending_orders = database_service.get_orders(statuses=["pending"])
        self.assertTrue(all(order["order_status"] == "pending" for order in pending_orders))

    def test_get_order_details_returns_line_items(self):
        order = database_service.get_order_details(1)
        self.assertIsNotNone(order)
        self.assertGreaterEqual(len(order["items"]), 1)
        self.assertIn("item_name", order["items"][0])


if __name__ == "__main__":
    unittest.main()
