from datetime import datetime


class ExpiryAlerts:
    """Provides methods to check for expiring or expired items."""

    def check_expiring(self, inventory, within_days: int = 3):
        """
        Return a list of items that will expire within the next 'within_days' days.
        """
        return [
            item
            for item in inventory.items.values()
            if item.is_expiring_within(within_days)
        ]

    def mark_expired(self, inventory):
        """Return a list of items that are already expired."""
        return [item for item in inventory.items.values() if item.is_expired()]

    def days_until_expiry(self, item) -> int:
        """Return the number of days until the item expires."""
        return (item.expiry_date - datetime.today()).days
