import json


class InventoryPersistence:
    """Provides loading and saving functionality for inventory."""

    @staticmethod
    def save_inventory(inventory, path: str = "inventory.json") -> None:
        """Save inventory to a JSON file."""
        data = {}
        for name, item in inventory.items.items():
            data[name] = {
                "quantity": item.quantity,
                "unit": item.unit,
                "expiry_date": item.expiry_date.strftime("%Y-%m-%d"),
            }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_inventory(inventory, path: str = "inventory.json") -> None:
        """Load inventory from a JSON file if it exists."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
            for name, info in data.items():
                inventory.add_item(
                    name,
                    info["quantity"],
                    info["unit"],
                    info["expiry_date"],
                )
        except FileNotFoundError:
            # If there is no file yet, just do nothing
            pass

    @staticmethod
    def inventory_to_dict(inventory) -> dict:
        """Convert current inventory into a plain Python dictionary."""
        result = {}
        for name, item in inventory.items.items():
            result[name] = {
                "quantity": item.quantity,
                "unit": item.unit,
                "expiry_date": item.expiry_date.strftime("%Y-%m-%d"),
            }
        return result
