import os
import unittest
from unittest.mock import patch

from freshfridge.inventory.operations import InventoryOperations
from freshfridge.reporting.base_report import BaseReport
from freshfridge.reporting.shopping_list import ShoppingListReport


def build_sample_inventory():
    inv = InventoryOperations()
    inv.add_item("Milk",   2,  "L",    "2025-12-18")
    inv.add_item("Eggs",   12, "pcs",  "2025-12-20")
    inv.add_item("Butter", 1,  "pack", "2025-12-30")
    inv.add_item("Apples", 5,  "pcs",  "2025-12-29")
    inv.add_item("Cheese", 0,  "block","2025-12-25")
    return inv


class TestShoppingListReport(unittest.TestCase):

    def setUp(self):
        self.inventory = build_sample_inventory()
        base_report = BaseReport(self.inventory)
        # ShoppingListReport inherits from BaseReport
        self.report = ShoppingListReport(base_report.inventory)

        # thresholds: how much we want to have for each item
        self.thresholds = {
            "Milk": 3,      # need 1 more
            "Eggs": 10,     # already enough
            "Butter": 1,    # need 1
            "Cheese": 2,    # need 1
        }

        self.shopping_list = self.report.generate_shopping_list(self.thresholds)

    def test_generate_shopping_list_contents(self):
        # Only items below threshold should appear
        names = [s["name"] for s in self.shopping_list]
        self.assertCountEqual(names, ["Milk", "Butter", "Cheese"])

        # Check one of the entries in detail
        butter = next(s for s in self.shopping_list if s["name"] == "Butter")
        self.assertEqual(butter["current_qty"], 0)
        self.assertEqual(butter["needed"], 1)

    @patch("builtins.print")
    def test_display_shopping_list_prints_something(self, mock_print):
        self.report.display_shopping_list(self.shopping_list)
        # at least one print call for header
        mock_print.assert_any_call("\n=== Recommended Shopping List ===")

    def test_export_shopping_list_writes_file(self):
        path = "test_shopping_list_output.txt"
        try:
            self.report.export_shopping_list(self.shopping_list, path=path)
            self.assertTrue(os.path.exists(path))

            with open(path, "r") as f:
                content = f.read()
            # check that at least one item name appears in the file
            self.assertIn("Milk", content)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
