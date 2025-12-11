from datetime import datetime
import unittest
from freshfridge.inventory.operations import InventoryOperations
from freshfridge.inventory.items import FreshItem
from freshfridge.reporting.base_report import BaseReport

class TestBaseReport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inventory = InventoryOperations()

        # Create 5 FreshItem objects
        cls.inventory.items = {
            "Milk": FreshItem("Milk", 2, "L", "2025-02-18"),
            "Eggs": FreshItem("Eggs", 12, "pcs", "2025-03-10"),
            "Butter": FreshItem("Butter", 1, "pack", "2025-01-05"),
            "Yogurt": FreshItem("Yogurt", 4, "cups", "2025-02-01"),
            "Cheese": FreshItem("Cheese", 1, "block", "2025-04-12")
        }

        cls.report = BaseReport(cls.inventory)

    def test_count_items(self):
        self.assertEqual(self.report.count_items(), 5)

    def test_list_all(self):
        items = self.report.list_all()
        self.assertEqual(len(items), 5)
        self.assertTrue(any(item.name == "Milk" for item in items))

    def test_get_item_names(self):
        names = self.report.get_item_names()
        expected = ["Milk", "Eggs", "Butter", "Yogurt", "Cheese"]
        self.assertCountEqual(names, expected)

if __name__ == "__main__":
    unittest.main()
