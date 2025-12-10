import unittest
from freshfridge.inventory.items import Item

class TestItems(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestItems class")

    def setUp(self):
        self.item = Item("Milk", 2, "L", "2025-02-18")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestItems class")

    def test_item_creation(self):
        self.assertEqual(self.item.name, "Milk")
        self.assertEqual(self.item.quantity, 2)
        self.assertEqual(self.item.unit, "L")
        self.assertEqual(self.item.expiry_date, "2025-02-18")

    def test_item_str(self):
        result = str(self.item)
        self.assertIn("Milk", result)
        self.assertIn("2", result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 5)
