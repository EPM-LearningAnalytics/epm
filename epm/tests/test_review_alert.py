"""
Test for review_alert.py 
"""

# Load libraries
import unittest
import epm.modeling.review_alert as ra


# test data_list for the unittest
class TestReviewAlert(unittest.TestCase):
    """
    class for testing review_alert.py
    """
    @classmethod
    def test_smoke(cls):
        """
        Simple smoke test to make sure function runs as expected.
        """
        id, feat_num = '4', '3'
        ra(id, feat_num)

    def test_args_out_of_range(self):
        """
        Edge test to give feat_num out of expected range.
        """
        id, feat_num = 3, 2
        with self.assertRaises(ValueError):
            ra(id, feat_num)

    def test_omit_variable(self):
        """
        Edge test not to give one variable
        """
        id, feat_num = 32, ''
        with self.assertRaises(TypeError):
            ra(id, feat_num)