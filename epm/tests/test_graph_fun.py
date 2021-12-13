"""
Tests for functions in graph_fun
"""

import unittest

from epm.graph.graph_data import session_agg, session_avg
from epm.graph.graph_fun import plot_log

class TestPlotLog(unittest.TestCase):
    """
    """
    def test_average_figure(self):
        """
        Smoke test to make sure the average log graph
        has the right type
        """
        # read datasets and prepare arguments
        df = session_agg()
        df_avg = session_avg(df)
        student = 1
        selected_activity = sorted( df['activity'].unique() )
        option = 'mouse_click_left'

        p = plot_log(df_avg, student, selected_activity, option, type='average')

        self.assertEqual(str(type(p)), "<class 'altair.vegalite.v4.api.Chart'>")


    def test_student_figure(self):
        """
        Smoke test to make sure the student log graph
        has the right type
        """
        df = session_agg()
        student = 1
        selected_activity = sorted( df['activity'].unique() )
        option = 'mouse_click_left'

        p = plot_log(df, student, selected_activity, option, type='student')

        self.assertEqual(str(type(p)), "<class 'altair.vegalite.v4.api.Chart'>")