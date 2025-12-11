class BaseReport:
    """Parent class for different types of reports."""

    def __init__(self, inventory):
        self.inventory = inventory

    def count_items(self) -> int:
        """Return the number of distinct items in the inventory."""
        return len(self.inventory.items)

    def list_all(self):
        """Return a list of all FreshItem objects."""
        return self.inventory.list_items()

    def get_item_names(self):
        """Return a list of all item names."""
        return list(self.inventory.items.keys())
