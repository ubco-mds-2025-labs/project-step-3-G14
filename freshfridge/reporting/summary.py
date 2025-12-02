from .base_report import BaseReport


class SummaryReport(BaseReport):
    """Generates summary of refrigerator items."""

    def request_summary(self):
        """
        Return a list of dictionaries with item information.
        Each dict: {name, quantity, unit, expiry_date}
        """
        summary = []
        for item in self.inventory.items.values():
            summary.append({
                "name": item.name,
                "quantity": item.quantity,
                "unit": item.unit,
                "expiry_date": item.expiry_date.strftime("%Y-%m-%d"),
            })
        return summary

    def display_summary(self) -> None:
        """Print a formatted summary to the console."""
        print("\n=== Refrigerator Inventory Summary ===")
        for item in self.request_summary():
            print(
                f"{item['name']} — {item['quantity']} {item['unit']} "
                f"(expires {item['expiry_date']})"
            )
        print("=====================================\n")

    def get_total_quantity(self) -> float:
        """Return the sum of quantities of all items."""
        return sum(item.quantity for item in self.inventory.items.values())
