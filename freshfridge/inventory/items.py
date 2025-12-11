from datetime import datetime

class InvalidExpiryDateError(Exception):
    """Raised when the expiry date format is invalid."""
    pass

class BaseItem:
    """Parent class storing basic item information."""

    def __init__(self, name: str):
        self.name = name

    def rename(self, new_name: str) -> None:
        """Change the item name."""
        self.name = new_name


class FreshItem(BaseItem):
    """
    Child class with quantity, unit, and expiry date.

    Demonstrates inheritance (BaseItem -> FreshItem).
    """

    def __init__(self, name: str, quantity: float, unit: str, expiry_date: str):
        super().__init__(name)
        self.quantity = quantity
        self.unit = unit
        try:
            self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError as e:
            raise InvalidExpiryDateError(
                f"Invalid expiry date format: '{expiry_date}'. Must be YYYY-MM-DD"
            ) from e

    def reduce_quantity(self, amount: float) -> None:
        """Reduce quantity by a given amount (not going below zero)."""
        self.quantity = max(0, self.quantity - amount)

    def is_expiring_within(self, days: int) -> bool:
        """Return True if the item expires within the next 'days' days."""
        return (self.expiry_date - datetime.today()).days <= days

    def is_expired(self) -> bool:
        """Return True if the item is already expired."""
        return self.expiry_date < datetime.today()
