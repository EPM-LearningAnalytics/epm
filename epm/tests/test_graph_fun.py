"""
Tests for functions in graph_fun
"""

import unittest

from epm.graph.graph_data import *
from epm.graph.graph_fun import *

class TestPlotMid(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        plot_mid(mid_avg().head())

    def test_input(self):
        """
        Simple smoke test to make sure function runs.
        """
        plot_mid(1)

    def test_input_structure(self):
        """
        Simple smoke test to make sure function runs.
        """
        plot_mid(mid_avg().drop(['Student Id']))

class TestPlotFinal(unittest.TestCase):
    """
    """
    @staticmethod
    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        data=final_mid(final_step_1())
        plot_final(data.head())

    def test_final_input(self):
        """
        Simple smoke test to make sure function runs.
        """
        plot_final(1)

    def test_final_input_structure(self):
        """
        Simple smoke test to make sure function runs.
        """
        data=final_avg(final_step_1())
        plot_final(data.drop(['Student ID']))