class LowStockAlerts:
    """Provides low-stock alert functionality."""

    def low_stock_alert(self, inventory, thresholds: dict):
        """Return list of (name, current_qty, threshold) for items below threshold."""
        if not isinstance(thresholds, dict):
            raise TypeError("thresholds must be a dictionary")
        alerts = []
        for name, item in inventory.items.items():
            if name in thresholds and item.quantity < thresholds[name]:
                alerts.append((name, item.quantity, thresholds[name]))
        return alerts

    def update_thresholds(self, thresholds: dict, new_thresholds: dict) -> dict:
        """Update a thresholds dictionary with new values."""
        thresholds.update(new_thresholds)
        return thresholds

    def items_at_zero(self, inventory):
        """Return list of items that have quantity equal to zero."""
        return [item for item in inventory.items.values() if item.quantity == 0]
