"""
Tests for the knn function
"""
import os
import unittest
cwd = os.getcwd()
print(cwd)
from epm.data_prep import log_prep
from epm.data_prep.log_prep import *

class TestLogPrep(unittest.TestCase):
    """
    Unittest class for test_knn.py
    """
    def test_smoke(self):
        """
        Simple smoke test
        """
        log_prep.main()

test = TestLogPrep()
test.test_smoke()