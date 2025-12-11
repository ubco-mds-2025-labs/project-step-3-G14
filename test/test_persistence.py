import os
import tempfile
import unittest

from freshfridge.inventory.operations import InventoryOperations
from freshfridge.inventory.persistence import InventoryPersistence


def build_sample_inventory() -> InventoryOperations:
    """Helper to create a small inventory with a few items."""
    inv = InventoryOperations()
    # expiry_date is a string; FreshItem converts it to datetime internally
    inv.add_item("Milk", 2, "L", "2025-12-18")
    inv.add_item("Eggs", 12, "pcs", "2025-12-20")
    return inv


class TestInventoryPersistence(unittest.TestCase):
    def setUp(self):
        self.inventory = build_sample_inventory()

    def test_inventory_to_dict_structure(self):
        """inventory_to_dict should return the expected plain dict."""
        result = InventoryPersistence.inventory_to_dict(self.inventory)

        # We expect both items to be present
        self.assertIn("Milk", result)
        self.assertIn("Eggs", result)

        milk = result["Milk"]
        self.assertEqual(milk["quantity"], 2)
        self.assertEqual(milk["unit"], "L")
        # dates are stored as strings in YYYY-MM-DD
        self.assertEqual(milk["expiry_date"], "2025-12-18")

    def test_save_and_load_inventory_roundtrip(self):
        """Saving then loading should reproduce the same items."""
        # create a temporary file path
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)  # we only need the path; save_inventory will reopen it

        try:
            # Save current inventory
            InventoryPersistence.save_inventory(self.inventory, path)

            # Load into a *new* InventoryOperations instance
            new_inventory = InventoryOperations()
            InventoryPersistence.load_inventory(new_inventory, path)

            # Both items should have been restored
            self.assertEqual(len(new_inventory.items), 2)
            self.assertIn("Milk", new_inventory.items)
            self.assertIn("Eggs", new_inventory.items)

            self.assertEqual(new_inventory.items["Milk"].quantity, 2)
            self.assertEqual(new_inventory.items["Milk"].unit, "L")
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_load_inventory_missing_file_does_nothing(self):
        """load_inventory should silently ignore missing files."""
        new_inventory = InventoryOperations()
        # Make sure the file really doesn't exist
        path = os.path.join(tempfile.gettempdir(), "this_file_should_not_exist.json")
        if os.path.exists(path):
            os.remove(path)

        # Should not raise, and inventory should stay empty
        InventoryPersistence.load_inventory(new_inventory, path)
        self.assertEqual(len(new_inventory.items), 0)


if __name__ == "__main__":
    unittest.main()
