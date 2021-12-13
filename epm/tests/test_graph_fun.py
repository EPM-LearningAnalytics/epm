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
        activity = sorted( df['activity'].unique() )
        option = 'mouse_click_left'

        p = plot_log(df_avg, student, activity, option, type='average')

        self.assertEqual(str(type(p)), "<class 'altair.vegalite.v4.api.Chart'>")


    def test_student_figure(self):
        """
        Smoke test to make sure the student log graph
        has the right type
        """
        # read datasets and prepare arguments
        df = session_agg()
        student = 1
        activity = sorted( df['activity'].unique() )
        option = 'mouse_click_left'

        p = plot_log(df, student, activity, option, type='student')

        self.assertEqual(str(type(p)), "<class 'altair.vegalite.v4.api.Chart'>")
    
    def test_plot_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input type is neither 'average' nor 'student'
        """
        with self.assertRaises(ValueError):
            df = session_agg()
            student = 1
            activity = sorted( df['activity'].unique() )
            option = 'mouse_click_left'
            type='individual'

            plot_log(df, student, activity, option, type)
    
    def test_data_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data is not the desired one
        """
        with self.assertRaises(ValueError):
            df = session_agg()
            student = 1
            activity = sorted( df['activity'].unique())
            option = 'mouse_click_left'

            plot_log(df, student, activity, option, type='average')
            
