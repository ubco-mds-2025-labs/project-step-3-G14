import unittest
from freshfridge.alerts.expiry import check_expiring
from freshfridge.inventory.items import Item

class TestExpiry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestExpiry class")

    def setUp(self):
        self.items = [
            Item("Yogurt", 1, "cup", "2025-02-10"),
            Item("Bread", 1, "loaf", "2025-05-10")
        ]

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestExpiry class")

    def test_expiry_detects_near_items(self):
        result = check_expiring(self.items, days=30)
        self.assertIn("Yogurt", result)
        self.assertNotIn("Bread", result)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)

    def test_expiry_no_near_items(self):
        result = check_expiring(self.items, days=1)
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)
        self.assertNotIn("Yogurt", result)
        self.assertNotIn("Bread", result)
