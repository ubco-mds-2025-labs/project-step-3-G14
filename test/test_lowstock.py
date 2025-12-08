import unittest
from freshfridge.alerts.lowstock import check_low_stock
from freshfridge.inventory.items import Item

class TestLowStock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestLowStock class")

    def setUp(self):
        self.items = {
            "Apple": Item("Apple", 1, "pcs", "2025-03-10"),
            "Orange": Item("Orange", 10, "pcs", "2025-03-20")
        }

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestLowStock class")

    def test_detect_low_stock(self):
        result = check_low_stock(self.items, threshold=5)
        self.assertIn("Apple", result)
        self.assertNotIn("Orange", result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_no_low_stock(self):
        result = check_low_stock(self.items, threshold=0)
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
        self.assertNotIn("Apple", result)
        self.assertNotIn("Orange", result)
