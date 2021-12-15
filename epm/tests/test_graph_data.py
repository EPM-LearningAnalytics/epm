"""
Tests for functions in graph_data
"""

import unittest

from epm.graph.graph_data import session_agg, session_avg
from epm.graph.graph_data import mid_avg, mid_hist, mid_summary


class TestSessionAgg(unittest.TestCase):
    """
    Test for function session_agg
    """
    def test_smoke(self):
        """
        smoke test to make sure function runs.
        """
        session_agg()


class TestSessionAvg(unittest.TestCase):
    """
    Test for function session_avg
    """
    def test_smoke(self):
        """
        smoke test to make sure function runs.
        """
        log_session = session_agg()
        session_avg(log_session)

    def test_data_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data type is not the desired one
        """
        with self.assertRaises(ValueError):
            log_session = 1
            session_avg(log_session)

    def test_data_column(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data does not have the correct column
        """
        with self.assertRaises(ValueError):
            log_session = session_agg()
            session_avg(log_session.drop(columns=['activity']))


class TestMidAvg(unittest.TestCase):
    """
    Test for function mid_avg
    """
    def test_smoke(self):
        """
        Smoke test to make sure function runs.
        """
        mid_avg()


class TestMidHist(unittest.TestCase):
    """
    Test for function mid_avg
    """
    def test_smoke(self):
        """
        Smoke test to make sure function runs.
        """
        mid_hist(2)

    def test_data_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data type is not the desired one
        """
        with self.assertRaises(ValueError):
            log_session = list((1, 2))
            mid_hist(log_session)

    def test_input_right_session(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data does not have the correct column
        """
        with self.assertRaises(ValueError):
            mid_hist(1)


class TestMidSummary(unittest.TestCase):
    """
    Test for function mid_avg
    """
    def test_smoke(self):
        """
        Smoke test to make sure function runs.
        """
        student = 1
        data_for_hist = mid_hist(2)
        mid_summary(student, data_for_hist)

    def test_parameter1_data_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data type is not the desired one
        """
        with self.assertRaises(ValueError):
            student = list((1, 2))
            data_for_hist = mid_hist(2)
            mid_summary(student, data_for_hist)

    def test_parameter2_data_type(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data type is not the desired one
        """
        with self.assertRaises(ValueError):
            student = 1
            data_for_hist = 1
            mid_summary(student, data_for_hist)

    def test_data_column(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data does not have the correct column
        """
        with self.assertRaises(ValueError):
            student = 1
            data_for_hist = mid_hist(2)
            mid_summary(student, data_for_hist.drop(columns=['Session_']))

    def test_student_in(self):
        """
        Edge test to make sure the function throws a ValueError
        when the input data does not have the correct column
        """
        with self.assertRaises(ValueError):
            student = 500
            data_for_hist = mid_hist(2)
            mid_summary(student, data_for_hist)
