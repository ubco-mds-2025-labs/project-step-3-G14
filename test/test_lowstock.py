import unittest
from freshfridge.alerts.lowstock import LowStockAlerts
from freshfridge.inventory.operations import InventoryOperations

class TestLowStock(unittest.TestCase):

    def setUp(self):
        self.inventory = InventoryOperations()
        self.inventory.add_item("Apple", 3, "pcs", "2025-12-20")
        self.inventory.add_item("Orange", 10, "pcs", "2025-12-25")
        self.alerts = LowStockAlerts()

    def test_low_stock_alert(self):
        thresholds = {"Apple": 5, "Orange": 5}
        result = self.alerts.low_stock_alert(self.inventory, thresholds)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("Apple", 3, 5))

    def test_items_at_zero(self):
        self.inventory.add_item("Empty", 1, "pcs", "2025-12-20")
        self.inventory.use_item("Empty", 1)  
        zero_items = self.alerts.items_at_zero(self.inventory)
        self.assertEqual(len(zero_items), 1)
        self.assertEqual(zero_items[0].name, "Empty")

    def test_no_low_stock(self):
        thresholds = {"Apple": 2, "Orange": 8}
        result = self.alerts.low_stock_alert(self.inventory, thresholds)
        self.assertEqual(len(result), 0)