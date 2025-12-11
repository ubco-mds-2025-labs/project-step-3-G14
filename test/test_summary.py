import unittest
from datetime import datetime, timedelta
from io import StringIO
from contextlib import redirect_stdout

from freshfridge.inventory.operations import InventoryOperations
from freshfridge.reporting.summary import SummaryReport


def make_sample_inventory():
    inventory = InventoryOperations()
    future = (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d")

    inventory.add_item("Milk",   2,  "L",    future)
    inventory.add_item("Eggs",   12, "pcs",  future)
    inventory.add_item("Apple",  5,  "pcs",  future)
    inventory.add_item("Yogurt", 4,  "cups", future)
    inventory.add_item("Butter", 1,  "pack", future)

    return inventory


class TestSummaryReport(unittest.TestCase):

    def setUp(self):
        self.inventory = make_sample_inventory()
        self.report = SummaryReport(self.inventory)

    def tearDown(self):
        self.inventory = None
        self.report = None

    def test_request_summary_returns_all_items(self):
        summary = self.report.request_summary()

        self.assertEqual(len(summary), 5)

        first = summary[0]
        for key in ["name", "quantity", "unit", "expiry_date"]:
            self.assertIn(key, first)

        # expiry_date should be a string in YYYY-MM-DD format
        self.assertRegex(first["expiry_date"], r"\d{4}-\d{2}-\d{2}")

    def test_get_total_quantity(self):
        total = self.report.get_total_quantity()
        # 2 + 12 + 5 + 4 + 1 = 24
        self.assertEqual(total, 24)

    def test_display_summary_prints_items(self):
        buf = StringIO()
        with redirect_stdout(buf):
            self.report.display_summary()

        output = buf.getvalue()
        self.assertIn("Refrigerator Inventory Summary", output)
        self.assertIn("Milk", output)
        self.assertIn("Eggs", output)


if __name__ == "__main__":
    unittest.main()
