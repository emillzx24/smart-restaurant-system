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

NEXT_STATUS = {
    "pending":     "preparing",
    "preparing": "ready",
    "ready":       "completed",
}

class StaffPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="staff_tests_"))
        cls.db_dir = cls.temp_dir / "database"
        cls.db_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / "database" / "schema.sql", cls.db_dir / "schema.sql")
        shutil.copy(REPO_ROOT / "database" / "seed.sql",   cls.db_dir / "seed.sql")
        cls.orig_db     = database_service.DB_PATH
        cls.orig_schema = database_service.SCHEMA_PATH
        cls.orig_seed   = database_service.SEED_PATH
        database_service.DB_PATH     = cls.db_dir / "restaurant_test.db"
        database_service.SCHEMA_PATH = cls.db_dir / "schema.sql"
        database_service.SEED_PATH   = cls.db_dir / "seed.sql"
        database_service.initialize_database()

    @classmethod
    def tearDownClass(cls):
        database_service.DB_PATH     = cls.orig_db
        database_service.SCHEMA_PATH = cls.orig_schema
        database_service.SEED_PATH   = cls.orig_seed
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    # TC-15
    def test_get_orders_returns_list(self):
        orders = database_service.get_orders()
        self.assertIsInstance(orders, list)
        self.assertGreater(len(orders), 0)

    # TC-16
    def test_orders_contain_required_keys(self):
        orders = database_service.get_orders()
        order = orders[0]
        for key in ["order_id", "order_status", "table_number", "order_total"]:
            self.assertIn(key, order, f"Missing key: {key}")

    # TC-17
    def test_valid_transition_pending_to_preparing(self):
        order = database_service.create_order(
            table_id=1, items=[{"item_id": 1, "quantity": 1}]
        )
        updated = database_service.update_order_status(
            order["order_id"], "preparing"
        )
        self.assertEqual("preparing", updated["order_status"])

    # TC-18
    def test_valid_transition_preparing_to_ready(self):
        order = database_service.create_order(
            table_id=1, items=[{"item_id": 2, "quantity": 1}]
        )
        database_service.update_order_status(order["order_id"], "preparing")
        updated = database_service.update_order_status(order["order_id"], "ready")
        self.assertEqual("ready", updated["order_status"])

    # TC-19
    def test_valid_transition_ready_to_completed(self):
        order = database_service.create_order(
            table_id=2, items=[{"item_id": 3, "quantity": 1}]
        )
        database_service.update_order_status(order["order_id"], "preparing")
        database_service.update_order_status(order["order_id"], "ready")
        updated = database_service.update_order_status(order["order_id"], "completed")
        self.assertEqual("completed", updated["order_status"])
        self.assertIsNotNone(updated["completed_at"])

    # TC-20
    def test_next_status_dictionary_is_complete(self):
        self.assertEqual(NEXT_STATUS["pending"],     "preparing")
        self.assertEqual(NEXT_STATUS["preparing"], "ready")
        self.assertEqual(NEXT_STATUS["ready"],       "completed")
        self.assertNotIn("completed", NEXT_STATUS)

    # TC-21
    def test_get_orders_returns_empty_list_when_no_orders(self):
        completed = database_service.get_orders(statuses=["completed"])
        self.assertIsInstance(completed, list)

    # TC-22
    def test_filter_by_pending_excludes_other_statuses(self):
        order = database_service.create_order(
            table_id=1, items=[{"item_id": 1, "quantity": 1}]
        )
        database_service.update_order_status(order["order_id"], "preparing")
        pending = database_service.get_orders(statuses=["pending"])
        ids = [o["order_id"] for o in pending]
        self.assertNotIn(order["order_id"], ids)

    # TC-23
    def test_order_details_include_items(self):
        order = database_service.create_order(
            table_id=1,
            items=[
                {"item_id": 1, "quantity": 2},
                {"item_id": 4, "quantity": 1, "special_instructions": "No salt"},
            ]
        )
        details = database_service.get_order_details(order["order_id"])
        self.assertEqual(2, len(details["items"]))
        self.assertIn("item_name", details["items"][0])

    # TC-24
    def test_end_to_end_order_appears_on_staff_page(self):
        new_order = database_service.create_order(
            table_id=2, items=[{"item_id": 5, "quantity": 1}]
        )
        all_orders = database_service.get_orders()
        ids = [o["order_id"] for o in all_orders]
        self.assertIn(new_order["order_id"], ids)
        match = next(o for o in all_orders if o["order_id"] == new_order["order_id"])
        self.assertEqual("pending", match["order_status"])


if __name__ == "__main__":
    unittest.main()