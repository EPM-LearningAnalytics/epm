"""
Tests for functions in graph_fun
"""

import unittest

from epm.graph.graph_data import *
from epm.graph.graph_fun import *

class TestPlotLog(unittest.TestCase):
    """
    Tests for plot_log function
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


class TestPlotMid(unittest.TestCase):
    """
    Tests for plotting intermediate line plot function
    """
    def test_average_figure(self):
        """
        Smoke test to make sure the intermediate graph
        has the right type
        """
        # read datasets and prepare arguments
        all, area = mid_avg()
        student = 1
        all = all[all['Student Id'].isin(['Average',str(student)])]

        m = plot_mid(all, area)

        self.assertEqual(str(type(m)), "<class 'altair.vegalite.v4.api.LayerChart'>")
    
    def test_avg_size(self):
        """
        Edge test to make sure the function throws a ValueError when
        area_data parameter has the wrong value
        """
        with self.assertRaises(ValueError):
            all= mid_avg()[0]
            plot_mid(all, all)


class TestPlotMidHist(unittest.TestCase):
    """
    Tests for plotting intermidiate histogram function
    """
    def test_hist_figure(self):
        """
        Smoke test to make sure the histogram graph
        has the right type
        """
        # read datasets and prepare arguments
        session = 2
        student = 1
        data_for_hist = mid_hist(session)
        data_summary = mid_summary(student, data_for_hist)

        p = plot_mid_hist(session, student, data_for_hist, data_summary)

        self.assertEqual(str(type(p)), "<class 'altair.vegalite.v4.api.LayerChart'>")

    def test_data_hist(self):
        """
        Edge test to make sure it throws a ValueError
        when the data_for_hist has the wrong dim
        """
        with self.assertRaises(ValueError):
            session = 2
            student = 1
            data_for_hist = mid_hist(session)
            data_summary = mid_summary(student, data_for_hist)
            plot_mid_hist(session, student, data_summary, data_for_hist)
