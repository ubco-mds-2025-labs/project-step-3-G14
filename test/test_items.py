import unittest

from datetime import datetime, timedelta
from freshfridge.inventory.items import FreshItem

class TestFreshItem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestFreshItem class")

    def setUp(self):
        future_date = "2025-12-18"
        self.item = FreshItem("Milk", 2, "L", future_date)

    def tearDown(self):
        self.item = None

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestFreshItem class")

    def test_item_creation(self):
        self.assertEqual(self.item.name, "Milk")
        self.assertEqual(self.item.quantity, 2.0)
        self.assertEqual(self.item.unit, "L")

        self.assertIsInstance(self.item.expiry_date, datetime)

    def test_rename(self):
        self.item.rename("Soy Milk")
        self.assertEqual(self.item.name, "Soy Milk")

    def test_reduce_quantity(self):
        self.item.reduce_quantity(1)
        self.assertAlmostEqual(self.item.quantity, 1)

        self.item.reduce_quantity(10)  # should floor at 0
        self.assertEqual(self.item.quantity, 0)

    def test_is_expired_true(self):
        yesterday = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
        expired_item = FreshItem("Yogurt", 1, "cup", yesterday)
        self.assertTrue(expired_item.is_expired())

    def test_is_expired_false(self):
        tomorrow = (datetime.today().date() + timedelta(days=1)).strftime("%Y-%m-%d")
        fresh_item = FreshItem("Yogurt", 1, "cup", tomorrow)
        self.assertFalse(fresh_item.is_expired())

    def test_is_expiring_within(self):
        in_5_days = (datetime.today().date() + timedelta(days=5)).strftime("%Y-%m-%d")
        cheese = FreshItem("Cheese", 1, "block", in_5_days)

        # within 7 days → True
        self.assertTrue(cheese.is_expiring_within(7))
        # within 3 days → False
        self.assertFalse(cheese.is_expiring_within(3))


if __name__ == "__main__":
    unittest.main()
