#!/usr/bin/env python

# coding: utf-8

"""
A module that tests log_prep.py
"""

# Load libraries
import unittest
import pandas as pd
import data_prep.log_prep as lp

# test data_list for the unittest


# test data_list for the unittest
class TestMLmodling(unittest.TestCase):
    """
    class for testing ml_modeling.py.

    Parameters
    ----------
    data_list, final_1st, final_2nd, mid_100, final_100, grades
    : A pandas dataframe including intermediate scores or/and final grades
    """
    # Test for read_file
    def test_edge_read_file(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'file_dir' is not a string.
        """
        file_dir = [1, 2, 3]
        with self.assertRaises(ValueError):
            lp.read_file(file_dir)

    # Test for feature_manipulation
    def test_edge_feature_manipulation(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'data_list' is a simple list.
        """
        data_list = [7, 8, 9]
        with self.assertRaises(ValueError):
            lp.feature_manipulation(data_list)

    # Test for feature_standardization
    def test_edge_feature_standardization(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'data_list' is not a list.
        """
        data_list = 'dataframe'
        with self.assertRaises(ValueError):
            lp.feature_standardization(data_list)

    # Tests for merge_all_data
    @classmethod
    def test_smoke_merge_all_data(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        session1 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [10, 5, 20, 21, 25],
                                 'CD': [15, 15, 22, 7, 17]})
        session2 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                                 'CD': [13, 12, 16, 4, 14]})
        session3 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                                 'CD': [13, 12, 16, 4, 14]})
        data_list = [session1, session2, session3]

        grades = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'MID1': [10, 5, 20, 21, 25],
                               'MID2': [13, 9, 19, 23, 22], 'MID3': [8, 7, 15, 18, 19],
                               'RES1': [1, 0, 0, 1, 1], 'RES2': [0, 1, 1, 1, 1],
                               'RES3': [0, 0, 0, 1, 1]})
        lp.merge_all_data(data_list, grades)

    def test_edge_merge_all_data(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'grades' is not a panda dataframe.
        """
        session1 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [10, 5, 20, 21, 25],
                                 'CD': [15, 15, 22, 7, 17]})
        session2 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                                 'CD': [13, 12, 16, 4, 14]})
        session3 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                                 'CD': [13, 12, 16, 4, 14]})
        data_list = [session1, session2, session3]

        grades = {'ID': [1, 2, 3, 4, 5], 'MID1': [10, 5, 20, 21, 25],
                  'MID2': [13, 9, 19, 23, 22], 'MID3': [8, 7, 15, 18, 19],
                  'RES1': [1, 0, 0, 1, 1], 'RES2': [0, 1, 1, 1, 1],
                  'RES3': [0, 0, 0, 1, 1]}

        with self.assertRaises(ValueError):
            lp.merge_all_data(data_list, grades)

    # Tests for save_grades
    def test_edge_save_data(self):
        """
        Edge test to make sure the function throws a ValueError
        when 'data_list' is not a panda dataframe.
        """
        data_list = {7, 8, 9}
        with self.assertRaises(ValueError):
            lp.save_data(data_list, save_dir='EPM_dataset/Data/')
