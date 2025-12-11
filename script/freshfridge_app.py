"""
Interactive, user-friendly command-line UI for the FreshFridge package.

Users can type simple commands like:
- add  : add a new item
- use  : consume part of an item
- show : see what is currently in the fridge
- exp  : check items that are expiring soon
- low  : manage low-stock thresholds and see low-stock items
- shop : generate and view a shopping list
- help : see all available commands
- quit : save and exit

This file demonstrates how to use the FreshFridge package for DATA 533 Step 3.
"""

# freshfridge_app.py
from datetime import datetime
from freshfridge.inventory.operations import InventoryOperations
from freshfridge.inventory.persistence import InventoryPersistence
from freshfridge.alerts.expiry import ExpiryAlerts
from freshfridge.alerts.lowstock import LowStockAlerts
from freshfridge.reporting.summary import SummaryReport
from freshfridge.reporting.shopping_list import ShoppingListReport
from freshfridge.inventory.items import InvalidExpiryDateError  

INVENTORY_PATH = "inventory_app.json"
SHOPPING_LIST_PATH = "shopping_list_app.txt"

INVENTORY_PATH = "inventory_app.json"
SHOPPING_LIST_PATH = "shopping_list_app.txt"


def print_welcome():
    print("=" * 50)
    print(" Welcome to FreshFridge 🧊")
    print("- Keep track of what's inside your fridge")
    print("- Monitor expiry dates and low-stock items")
    print("- Generate a shopping list when you need to restock")
    print("=" * 50)
    print("Type 'help' to see a list of commands.\n")


def print_help():
    print("\nAvailable commands:")
    print("  add   - Add a new item to the fridge")
    print("  use   - Use some quantity of an existing item")
    print("  show  - Show a summary of all items")
    print("  exp   - See items that are expiring soon")
    print("  low   - Set thresholds and see low-stock items")
    print("  shop  - Generate and (optionally) export a shopping list")
    print("  help  - Show this help message again")
    print("  quit  - Save your inventory and exit the program\n")


def handle_add(inventory: InventoryOperations):
    print("\n[ADD ITEM]")
    name = input("Item name: ").strip()
    if not name:
        print("  ❌ Name cannot be empty.")
        return

    try:
        quantity = float(input("Quantity (e.g. 1, 2.5): ").strip())
    except ValueError:
        print("  ❌ Invalid quantity.")
        return

    unit = input("Unit (e.g. pieces, carton, kg): ").strip()
    expiry = input("Expiry date (YYYY-MM-DD): ").strip()

    try:
        inventory.add_item(name, quantity, unit, expiry)
        print(f"  ✅ Item '{name}' added/updated.")
    except Exception as e:
        print(f"  ❌ Error adding item: {e}")


def handle_use(inventory: InventoryOperations):
    print("\n[USE ITEM]")
    if not inventory.items:
        print("  ℹ️ Inventory is empty. Nothing to use.")
        return

    name = input("Item name to use: ").strip()
    if name not in inventory.items:
        print(f"  ❌ Item '{name}' not found in inventory.")
        return

    try:
        quantity = float(input("Quantity to use: ").strip())
    except ValueError:
        print("  ❌ Invalid quantity.")
        return

    inventory.use_item(name, quantity)
    print(f"  ✅ Used {quantity} from '{name}'.")


def handle_show(summary_report: SummaryReport):
    print("\n[SHOW INVENTORY]")
    if not summary_report.inventory.items:
        print("  ℹ️ Your fridge is currently empty.")
    else:
        summary_report.display_summary()


def handle_expiry(inventory: InventoryOperations, expiry_alerts: ExpiryAlerts):
    print("\n[EXPIRY CHECK]")
    if not inventory.items:
        print("  ℹ️ Inventory is empty.")
        return

    days_str = input("Check items expiring within how many days? (default 3): ").strip()
    if days_str == "":
        days = 3
    else:
        try:
            days = int(days_str)
        except ValueError:
            print("  ❌ Invalid number of days.")
            return

    expiring_items = expiry_alerts.check_expiring(inventory, within_days=days)
    if not expiring_items:
        print(f"  ✅ No items expiring within {days} days.")
    else:
        print(f"  ⚠️ Items expiring within {days} days:")
        for item in expiring_items:
            print(f"   - {item.name} (quantity: {item.quantity}, unit: {item.unit})")


def handle_low_stock(inventory: InventoryOperations, lowstock_alerts: LowStockAlerts, thresholds: dict):
    print("\n[LOW-STOCK SETTINGS]")
    print("You can:")
    print("  1. Set/update a threshold for an item")
    print("  2. See low-stock items based on current thresholds")
    sub_choice = input("Choose 1 or 2 (or press Enter to go back): ").strip()

    if sub_choice == "1":
        name = input("Item name for threshold: ").strip()
        try:
            th = float(input("Minimum quantity you want to keep: ").strip())
        except ValueError:
            print("  ❌ Invalid threshold.")
            return
        thresholds[name] = th
        print(f"  ✅ Threshold for '{name}' set to {th}.")

    elif sub_choice == "2":
        if not thresholds:
            print("  ℹ️ No thresholds set yet. Please set at least one threshold first (option 1).")
            return
        low_items = lowstock_alerts.low_stock_alert(inventory, thresholds)
        if not low_items:
            print("  ✅ No items are currently below their thresholds.")
        else:
            print("  ⚠️ Low-stock items:")
            for name, qty, th in low_items:
                print(f"   - {name}: {qty} (threshold {th})")

    else:
        print("  ↩ Back to main menu.")


def handle_shopping_list(
    inventory: InventoryOperations,
    shopping_report: ShoppingListReport,
    thresholds: dict,
    export_path: str = SHOPPING_LIST_PATH,
):
    print("\n[SHOPPING LIST]")
    if not thresholds:
        print("  ℹ️ No thresholds set yet. Please use 'low' to set thresholds first.")
        return

    shopping_list = shopping_report.generate_shopping_list(thresholds)
    shopping_report.display_shopping_list(shopping_list)

    if not shopping_list:
        return

    do_export = input("Do you want to export this list to a file? (y/n): ").strip().lower()
    if do_export == "y":
        shopping_report.export_shopping_list(shopping_list, export_path)
        print(f"  ✅ Shopping list exported to '{export_path}'.")
    else:
        print("  ℹ️ Shopping list not exported.")


def main():
    inventory = InventoryOperations()
    expiry_alerts = ExpiryAlerts()
    lowstock_alerts = LowStockAlerts()
    summary_report = SummaryReport(inventory)
    shopping_report = ShoppingListReport(inventory)
    thresholds: dict[str, float] = {}  

    try:
        InventoryPersistence.load_inventory(inventory, INVENTORY_PATH)
        print("Inventory loaded successfully.")
    except ValueError as e:
        print(f"Warning: {e}. Starting with empty inventory.")
    except Exception as e:
        print(f"Unexpected error loading inventory: {e}. Starting with empty inventory.")

    print_welcome()

    while True:
        cmd = input("What would you like to do? (type 'help' for options): ").strip().lower()

        if cmd in ("quit", "q", "exit"):
            InventoryPersistence.save_inventory(inventory, INVENTORY_PATH)
            print(f"\n💾 Inventory saved to '{INVENTORY_PATH}'.")
            print("Goodbye! 👋")
            break

        elif cmd in ("help", "h", "?"):
            print_help()

        elif cmd in ("add", "a"):
            handle_add(inventory)

        elif cmd in ("use", "u"):
            handle_use(inventory)

        elif cmd in ("show", "s"):
            handle_show(summary_report)

        elif cmd in ("exp", "expiry", "e"):
            handle_expiry(inventory, expiry_alerts)

        elif cmd in ("low", "l"):
            handle_low_stock(inventory, lowstock_alerts, thresholds)

        elif cmd in ("shop", "shopping", "list"):
            handle_shopping_list(inventory, shopping_report, thresholds)

        else:
            print("❓ I did not understand that command. Type 'help' to see options.")


if __name__ == "__main__":
    main()
