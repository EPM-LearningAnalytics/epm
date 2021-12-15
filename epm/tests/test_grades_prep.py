#!/usr/bin/env python

# coding: utf-8

"""
A module that tests log_prep.py
"""

# Load libraries
import unittest
import pandas as pd
import data_prep.grades_prep as gp

# test data_list for the unittest


# test data_list for the unittest
class TestMLmodling(unittest.TestCase):
    """
    class for testing ml_modeling.py.

    Parameters
    ----------
    data_list: A list containing pandas dataframes
    """
    # Tests for read_grades
    def test_edge_read_grades(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'grades' is not a panda dataframe.
        """
        dir1 = [1, 2, 3]
        dir2 = [4, 5, 6]
        with self.assertRaises(ValueError):
            gp.read_grades(dir1, dir2)

    # Tests for final_manipulation
    def test_edge_final_manipulation(self):
        """
        Edge test to make sure the function throws a ValueError
        when the final_1st and final 2nd are not dataframes
        """
        final_1st = 'DUC_KS'
        final_2nd = [1, 2, 3]
        with self.assertRaises(ValueError):
            gp.final_manipulation(final_1st, final_2nd)

    # Tests for rebase_mid
    @classmethod
    def test_smoke_rebase_mid(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        mid_grades = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'MID2': [10, 5, 20, 21, 25],
                                   'MID3': [13, 9, 19, 23, 22], 'MID4': [8, 7, 15, 18, 19],
                                   'MID5': [8, 9, 10, 15, 12], 'MID6': [15, 4, 3, 5, 3]})
        gp.rebase_mid(mid_grades)

    def test_edge_rebase_mid(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'mid_grades' is not a panda dataframe.
        """
        mid_grades = [1, 2, 3]
        with self.assertRaises(ValueError):
            gp.rebase_mid(mid_grades)

    # Tests for merge_mid_final
    @classmethod
    def test_smoke_merge_mid_final(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        mid_100 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'MID1': [10, 5, 20, 21, 25],
                                'MID2': [13, 9, 19, 23, 22], 'MID3': [8, 7, 15, 18, 19],
                                'MID4': [8, 9, 10, 15, 12], 'MID5': [15, 4, 3, 5, 3],
                                'MID6': [20, 25, 13, 11, 22]})
        final_100 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'FIN1': [80, 90, 100, 55, 12],
                                  'FIN2': [90, 40, 33, 50, 35], 'FIN3': [22, 26, 30, 70, 90],
                                  'FIN4': [17, 18, 11, 13, 22], 'FIN5': [20, 25, 13, 11, 22],
                                  'FIN6': [20, 25, 13, 11, 22]})
        gp.merge_mid_final(mid_100, final_100)

    def test_edge_merge_mid_final(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'mid_grades' is not a panda dataframe.
        """
        mid_100 = [1, 2, 3]
        final_100 = [4, 5, 6]
        with self.assertRaises(ValueError):
            gp.merge_mid_final(mid_100, final_100)

    # Tests for standardize_grades
    @classmethod
    def test_smoke_standardize_grades(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        grades = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'MID1': [10, 5, 20, 21, 25],
                               'MID2': [13, 9, 19, 23, 22], 'MID3': [8, 7, 15, 18, 19],
                               'MID4': [8, 9, 10, 15, 12], 'MID5': [15, 4, 3, 5, 3],
                               'MID6': [20, 25, 13, 11, 22], 'FIN1': [80, 90, 100, 55, 12],
                               'FIN2': [90, 40, 33, 50, 35], 'FIN3': [22, 26, 30, 70, 90],
                               'FIN4': [17, 18, 11, 13, 22], 'FIN5': [20, 25, 13, 11, 22],
                               'FIN6': [20, 25, 13, 11, 22]})
        gp.standardize_grades(grades)

    def test_edge_standardize_grades(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'grades' is not a panda dataframe.
        """
        grades = [1, 2, 3]
        with self.assertRaises(ValueError):
            gp.standardize_grades(grades)

    # Tests for get_result
    @classmethod
    def test_get_result(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        grades = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'MID1': [10, 5, 20, 21, 25],
                               'MID2': [13, 9, 19, 23, 22], 'MID3': [8, 7, 15, 18, 19],
                               'MID4': [8, 9, 10, 15, 12], 'MID5': [15, 4, 3, 5, 3],
                               'MID6': [20, 25, 13, 11, 22], 'FIN1': [80, 90, 100, 55, 12],
                               'FIN2': [90, 40, 33, 50, 35], 'FIN3': [22, 26, 30, 70, 90],
                               'FIN4': [17, 18, 11, 13, 22], 'FIN5': [20, 25, 13, 11, 22],
                               'FIN6': [20, 25, 13, 11, 22]})
        gp.get_result(grades)

    def test_edge_get_result(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'grades' is not a panda dataframe.
        """
        grades = [1, 2, 3]
        with self.assertRaises(ValueError):
            gp.get_result(grades)

    # Tests for save_grades
    def test_edge_save_grades(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'grades' is not a panda dataframe.
        """
        grades = [1, 2, 3]
        with self.assertRaises(ValueError):
            gp.save_grades(grades, 'EPM_dataset/Data/')
