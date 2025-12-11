from .items import FreshItem


class InventoryOperations:
    """Handles adding, using, listing, and removing refrigerator items."""

    def __init__(self):
        # Dictionary: name -> FreshItem
        self.items = {}

    def add_item(self, name: str, quantity: float, unit: str, expiry_date: str) -> None:
        """Create or overwrite an item in the inventory."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items[name] = FreshItem(name, quantity, unit, expiry_date)

    def use_item(self, name: str, quantity: float) -> None:
        """Reduce the quantity of an item if it exists."""
        if name in self.items:
            self.items[name].reduce_quantity(quantity)

    def remove_item(self, name: str) -> None:
        """Completely remove an item from the inventory."""
        if name in self.items:
            del self.items[name]

    def list_items(self):
        """Return a list of all FreshItem objects."""
        return list(self.items.values())
