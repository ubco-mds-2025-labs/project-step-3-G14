import unittest
from freshfridge.inventory.operations import InventoryOperations
from freshfridge.inventory.items import FreshItem

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.inventory = InventoryOperations()

    def test_add_item(self):
        self.inventory.add_item("Eggs", 12, "pcs", "2025-12-20")
        self.assertIn("Eggs", self.inventory.items)
        item = self.inventory.items["Eggs"]
        self.assertIsInstance(item, FreshItem)
        self.assertEqual(item.quantity, 12)
        self.assertEqual(item.unit, "pcs")

    def test_use_item(self):
        self.inventory.add_item("Eggs", 12, "pcs", "2025-12-20")
        self.inventory.use_item("Eggs", 5)
        self.assertEqual(self.inventory.items["Eggs"].quantity, 7)

    def test_use_item_nonexistent(self):
        self.inventory.use_item("Nonexistent", 10)
        self.assertNotIn("Nonexistent", self.inventory.items)

    def test_remove_item(self):
        self.inventory.add_item("Milk", 1, "L", "2025-12-15")
        self.inventory.remove_item("Milk")
        self.assertNotIn("Milk", self.inventory.items)
        
    def test_add_item_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.add_item("Zero", 0, "pcs", "2025-12-20")