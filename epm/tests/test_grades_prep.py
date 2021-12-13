"""
Tests for the knn function
"""

import unittest
import numpy as np

from epm.data_prep import grades_prep
from epm.data_prep.grades_prep import *

class TestGradesPrep(unittest.TestCase):
    """
    Unittest class for test_knn.py
    """
    def test_smoke(self):
        """
        Simple smoke test
        """
        grades_prep.main()

test = TestGradesPrep()
test.test_smoke()