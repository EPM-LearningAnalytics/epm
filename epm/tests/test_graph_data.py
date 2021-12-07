"""
Tests for functions in graph_data
"""

import unittest

from epm.graph.graph_data import session_agg


class TestSessionAgg(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke():
        """
        Simple smoke test to make sure function runs.
        """
        session_agg()
    
    def test_data_dim(self):
        """
        One shot test to check if data has the required
        dimensions.
        """
    
