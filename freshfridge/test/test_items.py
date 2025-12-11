import unittest
from datetime import datetime
from freshfridge.inventory.items import FreshItem

class TestItems(unittest.TestCase):

    def setUp(self):
        self.item = FreshItem("Milk", 2.0, "L", "2025-02-18")

    def test_item_creation(self):
        self.assertEqual(self.item.name, "Milk")
        self.assertEqual(self.item.quantity, 2.0)
        self.assertEqual(self.item.unit, "L")
        self.assertEqual(self.item.expiry_date, datetime(2025, 2, 18))

    def test_reduce_quantity(self):
        self.item.reduce_quantity(0.5)
        self.assertEqual(self.item.quantity, 1.5)
        self.item.reduce_quantity(2.0)
        self.assertEqual(self.item.quantity, 0.0)

    def test_is_expiring_within(self):
        self.assertTrue(self.item.is_expiring_within(10000))  
        self.assertFalse(self.item.is_expiring_within(0))

    def test_is_expired(self):
        self.assertTrue(self.item.is_expired())