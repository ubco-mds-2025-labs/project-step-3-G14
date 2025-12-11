# test/test_suite.py
import unittest

def suite():
    """
    Automatically discover and run all test cases in the 'test/' directory.
    """
    loader = unittest.TestLoader()
    # Automatically find .py file with "test_" from test/
    suite = loader.discover(start_dir='test', pattern='test_*.py')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())