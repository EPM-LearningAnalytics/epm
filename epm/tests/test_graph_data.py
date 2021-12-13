"""
Tests for functions in graph_data
"""

import unittest

from epm.graph.graph_data import *


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
    
class TestMidAvg(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        mid_avg()
    
class TestFinalStepFirst(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        final_step_1()

class TestFinalAvg(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        final_avg(final_step_1())

    def test_input(self):
        """
        test that the input should be a dataframe
        """
        final_avg(1)

    def test_input_column(self):
        """
        test that the input dataframe should have a similar structure 
        to the output of graph.graph_data.final_step_1()
        """
        data = final_step_1().drop(['Student ID'])
        final_avg(data)
