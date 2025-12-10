import unittest

from test.test_items import TestItems
from test.test_operations import TestOperations
from test.test_expiry import TestExpiry
from test.test_lowstock import TestLowStock


def suite():
    """
    Build a test suite that includes all test classes
    for the FreshFridge package.
    """
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(TestItems))
    test_suite.addTests(loader.loadTestsFromTestCase(TestOperations))
    test_suite.addTests(loader.loadTestsFromTestCase(TestExpiry))
    test_suite.addTests(loader.loadTestsFromTestCase(TestLowStock))

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
