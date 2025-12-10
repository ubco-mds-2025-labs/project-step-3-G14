import unittest
from freshfridge.operations import add_item, use_item
from freshfridge.inventory.items import Item

class TestOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestOperations class")

    def setUp(self):
        self.inventory = {}
        self.item = Item("Eggs", 12, "pcs", "2025-02-20")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestOperations class")

    def test_add_item(self):
        add_item(self.inventory, self.item)
        self.assertIn("Eggs", self.inventory)
        self.assertEqual(self.inventory["Eggs"].quantity, 12)
        self.assertIsInstance(self.inventory["Eggs"], Item)
        self.assertEqual(len(self.inventory), 1)

    def test_use_item(self):
        add_item(self.inventory, self.item)
        use_item(self.inventory, "Eggs", 2)
        self.assertEqual(self.inventory["Eggs"].quantity, 10)
        self.assertGreater(self.inventory["Eggs"].quantity, 0)
        self.assertIsInstance(self.inventory["Eggs"], Item)
        self.assertNotEqual(self.inventory["Eggs"].quantity, 12)
