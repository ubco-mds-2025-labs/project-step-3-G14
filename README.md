# FreshFridge Package Function Documentation

## Group 14
### Yin-Wen Tsai, Jiaqi Yao, Sasivimol Sirijangkapattana

FreshFridge is a Python package designed to manage refrigerator inventory, generate reports, and provide alerts for expiring or low-stock items.  
This repository now includes both the Step 1 package implementation and the Step 2 unit test suite.

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

# 6. Unit Testing Structure (Step 2)

A new directory contains all unit tests written using Python’s `unittest` framework.

```text
test/
│
├── test_items.py
├── test_operations.py
├── test_expiry.py
├── test_lowstock.py
└── test_suite.py
```

### ✔ Each test class includes:
- `setUp()`, `tearDown()`
- `setUpClass()`, `tearDownClass()`
- ≥ 2 test cases
- ≥ 4 assertions per test case

### ✔ `test_suite.py`
Manually loads all test classes into a unified suite so they can run together:

```python
import unittest
from test_items import TestItems
from test_operations import TestOperations
from test_expiry import TestExpiryAlerts
from test_lowstock import TestLowStockAlerts

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestItems))
    suite.addTests(loader.loadTestsFromTestCase(TestOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestExpiryAlerts))
    suite.addTests(loader.loadTestsFromTestCase(TestLowStockAlerts))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```
---

# 7. Version Control Workflow (Step 2)

The team followed collaborative Git workflows:

Created new repository for Step 1 code

Each member cloned repo, created personal branch

Implemented unit tests independently

Opened Pull Requests

Reviewed & merged changes into main

Git history demonstrates equal contribution

---

# 8. How to Run Tests

```bash
cd freshfridge-project
python -m unittest discover test
```

or run the test suite file:

```bash
python test/test_suite.py
```

# 9. Summary

This repository now contains:

* Fully modular FreshFridge package (Step 1)

* Complete unittest-based test coverage (Step 2)

* Documented structure and collaborative Git history

The codebase demonstrates modular design, documentation, testability, and collaborative software development practices suitable for DATA 533.
