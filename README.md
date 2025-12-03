# FreshFridge Package Function Documentation

This document describes the structure of the FreshFridge package and explains the functionality of each module, class, and function.  
The purpose is to demonstrate how the package works internally for DATA 533 — Step 3.

---

# 1. Package Structure

```text
freshfridge/
│
├── inventory/
│ ├── init.py
│ ├── items.py
│ ├── operations.py
│ └── persistence.py
│
├── alerts/
│ ├── init.py
│ ├── expiry.py
│ └── lowstock.py
│
└── reporting/
  ├── init.py
  ├── base_report.py
  ├── summary.py
  └── shopping_list.py
```


The package is divided into three logical sub-packages:

- **inventory** — manages items stored in the refrigerator  
- **alerts** — checks expiry and low-stock warnings  
- **reporting** — generates summaries and shopping lists  

---

# 2. `inventory` Sub-Package

## 2.1 `items.py`
This module defines the core data model used to represent a food item.

### **Class: `BaseItem`**
Parent class representing a general item.

| Method | Description |
|--------|-------------|
| `__init__(name)` | Stores the item name. |
| `rename(new_name)` | Updates the item’s name. |

---

### **Class: `FreshItem(BaseItem)`**
Child class that inherits from `BaseItem`.  
Used for actual refrigerator items with quantity and expiry information.

| Method | Description |
|--------|-------------|
| `__init__(name, quantity, unit, expiry_date)` | Initializes a fresh item with quantity, measurement unit, and expiry date. |
| `reduce_quantity(amount)` | Decreases the quantity, preventing values below zero. |
| `is_expiring_within(days)` | Returns `True` if the item expires within the next *X* days. |
| `is_expired()` | Returns `True` if the expiry date has passed. |

---

## 2.2 `operations.py`
Manages the refrigerator inventory through a dictionary of `FreshItem` objects.

### **Class: `InventoryOperations`**

| Method | Description |
|--------|-------------|
| `__init__()` | Creates an empty inventory dictionary. |
| `add_item(name, quantity, unit, expiry_date)` | Adds or replaces an item in the inventory. |
| `use_item(name, quantity)` | Reduces the quantity of an item. |
| `remove_item(name)` | Deletes an item from the inventory. |
| `list_items()` | Returns a list of all `FreshItem` objects. |

---

## 2.3 `persistence.py`
Handles saving and loading the inventory from JSON.

### **Class: `InventoryPersistence`**

| Method | Description |
|--------|-------------|
| `save_inventory(inventory, path)` | Writes the current inventory to a JSON file. |
| `load_inventory(inventory, path)` | Reads a JSON file and reconstructs all items using `add_item()`. |
| `inventory_to_dict(inventory)` | Converts the entire inventory to a dictionary for serialization. |

These functions ensure that the fridge state persists between program runs.

---

# 3. `alerts` Sub-Package

## 3.1 `expiry.py`
Checks whether any items are close to expiring.

### **Class: `ExpiryAlerts`**

| Method | Description |
|--------|-------------|
| `check_expiring(inventory, within_days)` | Returns items that expire within the given number of days. |
| `mark_expired(inventory)` | Returns a list of already expired items. |
| `days_until_expiry(item)` | Calculates how many days remain before an item expires. |

---

## 3.2 `lowstock.py`
Manages low-stock alerts based on user-defined thresholds.

### **Class: `LowStockAlerts`**

| Method | Description |
|--------|-------------|
| `low_stock_alert(inventory, thresholds)` | Returns items whose quantity is below their threshold. |
| `update_thresholds(thresholds, new_thresholds)` | Updates the threshold dictionary. |
| `items_at_zero(inventory)` | Returns items with zero quantity remaining. |

---

# 4. `reporting` Sub-Package

## 4.1 `base_report.py`
Parent class for other reporting modules.

### **Class: `BaseReport`**

| Method | Description |
|--------|-------------|
| `count_items()` | Returns number of items in the inventory. |
| `list_all()` | Returns a list of all items. |
| `get_item_names()` | Returns names of all items in the inventory. |

---

## 4.2 `summary.py`
Creates human-readable summaries of the fridge contents.

### **Class: `SummaryReport (BaseReport)`**

| Method | Description |
|--------|-------------|
| `request_summary()` | Returns item information as a list of dictionaries. |
| `display_summary()` | Prints a formatted table-like overview. |
| `get_total_quantity()` | Sums quantities of all items. |

---

## 4.3 `shopping_list.py`
Creates and exports recommended shopping lists.

### **Class: `ShoppingListReport (BaseReport)`**

| Method | Description |
|--------|-------------|
| `generate_shopping_list(thresholds)` | Calculates which items should be restocked. |
| `display_shopping_list(list)` | Prints a human-friendly shopping list. |
| `export_shopping_list(list, path)` | Saves the list to a text file. |

---

# 5. How the Package Works (High-Level)

1. **Users interact with the program** through our interactive CLI (`freshfridge_app.py` will be done in the final step).  
2. **New items** are added through `InventoryOperations.add_item()`.  
3. **Quantities change** using `use_item()` and thresholds detect low-stock situations.  
4. **Expiry alerts** use date calculations inside `FreshItem` and `ExpiryAlerts`.  
5. **Data is saved** using JSON serialization inside `InventoryPersistence`.  
6. **Reports** help display fridge content and generate shopping lists.  
7. **On the next run**, the inventory is automatically reloaded.

This modular design demonstrates good software organization, separation of concerns, and proper use of Python packages.

---

# 6. Summary

This document explains all modules and functions required for understanding the FreshFridge package.  
It serves as the function reference required in DATA 533 Step 3.
