import unittest
from io import StringIO
from unittest.mock import patch
from freshfridge.inventory.operations import InventoryOperations
from freshfridge.reporting.shopping_list import ShoppingListReport

def build_sample_inventory():
    inv = InventoryOperations()
    inv.add_item("Milk", 2, "L", "2025-12-20")
    inv.add_item("Eggs", 12, "pcs", "2025-12-25")
    inv.add_item("Butter", 1, "pack", "2025-12-30")  
    inv.add_item("Cheese", 1, "pack", "2025-12-30")  
    inv.use_item("Butter", 1)
    inv.use_item("Cheese", 1)
    return inv

class TestShoppingListReport(unittest.TestCase):
    def setUp(self):
        self.inventory = build_sample_inventory()
        self.report = ShoppingListReport(self.inventory)

    def test_generate_shopping_list_contents(self):
        thresholds = {"Milk": 3, "Butter": 1, "Cheese": 1}
        shopping_list = self.report.generate_shopping_list(thresholds)
        self.assertEqual(len(shopping_list), 3)
        self.assertEqual(shopping_list[0]["name"], "Milk")
        self.assertEqual(shopping_list[0]["needed"], 1)
        self.assertEqual(shopping_list[1]["name"], "Butter")
        self.assertEqual(shopping_list[1]["needed"], 1)
        self.assertEqual(shopping_list[2]["name"], "Cheese")
        self.assertEqual(shopping_list[2]["needed"], 1)

    def test_display_shopping_list_prints_something(self):
        thresholds = {"Milk": 3, "Butter": 1}
        shopping_list = self.report.generate_shopping_list(thresholds)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.report.display_shopping_list(shopping_list)
            output = fake_out.getvalue()
            self.assertTrue(len(output) > 0)
            self.assertIn("Milk", output)

    def test_export_shopping_list_writes_file(self):
        thresholds = {"Milk": 3}
        shopping_list = self.report.generate_shopping_list(thresholds)

        self.report.export_shopping_list(shopping_list, "temp_shopping.txt")

        with open("temp_shopping.txt", "r") as f:
            content = f.read()
            self.assertIn("Milk", content)

        import os
        os.remove("temp_shopping.txt")


if __name__ == "__main__":
    unittest.main()
