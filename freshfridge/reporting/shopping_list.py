from .base_report import BaseReport


class ShoppingListReport(BaseReport):
    """Generates shopping list based on low-stock items."""

    def generate_shopping_list(self, thresholds: dict):
        """Return a list of shopping items."""
        if not isinstance(thresholds, dict):
            raise TypeError("thresholds must be a dictionary")
        shopping_list = []
        for name, item in self.inventory.items.items():
            if name in thresholds and item.quantity < thresholds[name]:
                shopping_list.append({
                    "name": name,
                    "current_qty": item.quantity,
                    "needed": thresholds[name] - item.quantity,
                })
        return shopping_list

    def display_shopping_list(self, shopping_list) -> None:
        """Print the shopping list in a readable format."""
        print("\n=== Recommended Shopping List ===")
        if not shopping_list:
            print("No items need to be purchased.")
        else:
            for s in shopping_list:
                print(
                    f"{s['name']}: need {s['needed']} "
                    f"(current {s['current_qty']})"
                )
        print("=================================\n")

    def export_shopping_list(self, shopping_list, path: str = "shopping_list.txt") -> None:
        """Export the shopping list to a text file."""
        with open(path, "w") as f:
            for s in shopping_list:
                f.write(f"{s['name']}: need {s['needed']} (current {s['current_qty']})\n")
