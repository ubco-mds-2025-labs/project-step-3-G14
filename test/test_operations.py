import unittest
from datetime import datetime, timedelta

from freshfridge.inventory.operations import InventoryOperations
from freshfridge.inventory.items import FreshItem


class TestInventoryOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestInventoryOperations class")

    def setUp(self):
        # new inventory for each test
        self.inventory = InventoryOperations()

        # use a future expiry date so the item is not expired
        future_date = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.inventory.add_item("Eggs", 12, "pcs", future_date)

    def tearDown(self):
        self.inventory = None

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestInventoryOperations class")

    def test_add_item(self):
        # Eggs should have been added in setUp
        self.assertIn("Eggs", self.inventory.items)

        item = self.inventory.items["Eggs"]
        self.assertIsInstance(item, FreshItem)
        self.assertEqual(item.name, "Eggs")
        self.assertEqual(item.quantity, 12)
        self.assertEqual(item.unit, "pcs")

    def test_use_item(self):
        # use 2 eggs
        self.inventory.use_item("Eggs", 2)
        item = self.inventory.items["Eggs"]
        self.assertEqual(item.quantity, 10)

        # using more than available should not go below 0
        self.inventory.use_item("Eggs", 100)
        self.assertEqual(item.quantity, 0)

    def test_remove_item(self):
        self.inventory.remove_item("Eggs")
        self.assertNotIn("Eggs", self.inventory.items)

    def test_list_items(self):
        items = self.inventory.list_items()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], FreshItem)
        self.assertEqual(items[0].name, "Eggs")


if __name__ == "__main__":
    unittest.main()
