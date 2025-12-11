# test/test_expiry.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from freshfridge.alerts.expiry import ExpiryAlerts
from freshfridge.inventory.operations import InventoryOperations

class TestExpiry(unittest.TestCase):

    def setUp(self):
        self.inventory = InventoryOperations()
        self.inventory.add_item("Yogurt", 1, "cup", "2025-12-15")
        self.inventory.add_item("Bread", 1, "loaf", "2026-05-10")
        self.alerts = ExpiryAlerts()

    def test_check_expiring(self):
        expiring = self.alerts.check_expiring(self.inventory, within_days=10)
        self.assertEqual(len(expiring), 1)
        self.assertEqual(expiring[0].name, "Yogurt")

    def test_mark_expired(self):
        expired = self.alerts.mark_expired(self.inventory)
        self.assertEqual(len(expired), 0)

        self.inventory.add_item("Old Milk", 1, "L", "2025-11-01")
        expired = self.alerts.mark_expired(self.inventory)
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0].name, "Old Milk")

    def test_days_until_expiry(self):
        yogurt = self.inventory.items["Yogurt"]
        with patch('freshfridge.alerts.expiry.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime(2025, 12, 10)  
            days = self.alerts.days_until_expiry(yogurt)
            self.assertEqual(days, 5)