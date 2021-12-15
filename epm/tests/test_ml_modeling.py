#!/usr/bin/env python

# coding: utf-8

"""
A module that tests ml_modeling.py
"""

# Load libraries
import unittest
import pandas as pd
import epm.modeling.ml_modeling as mm


# test data_list for the unittest
session1 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [10, 5, 20, 21, 25],
                         'CD': [15, 15, 22, 7, 17], 'Y': [1, 1, 0, 1, 0],
                         'MID1': [10, 5, 20, 21, 25]})
session2 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                         'CD': [13, 12, 16, 4, 14], 'Y': [1, 1, 0, 0, 0],
                         'MID2': [13, 9, 19, 23, 22]})
session3 = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'AB': [13, 9, 19, 23, 22],
                         'CD': [13, 12, 16, 4, 14], 'Y': [1, 0, 1, 0, 0],
                         'MID3': [13, 9, 19, 23, 22]})


# test data_list for the unittest
class TestMLmodling(unittest.TestCase):
    """
    class for testing ml_modeling.py.

    Parameters
    ----------
    data_list: A list containing pandas dataframes
               including sessions' and grades' data
    num_of_features: The number of features that a user wants to subset
    option: Different ways to subset the data_list
            'common': Subset common significant features across all sessions
            'different': Subset significant features from each session
    ml_model: A machine learning model that a user wants to fit
             'KNN': K-nearest neighbors
             'DT': Decision tree
             'RF': Randome forest
             'NB': Naive Bayes
             'LR': Logistic regression
             'SVC': Support vector classifier
    num_of_sessions: The timing when a user wants to form a group
    num_of_clusters: The number of clusters that a user wants to form
    """

    # Tests for subset_important_feature
    @classmethod
    def test_smoke_subset_important_features1(cls):
        """
        Simple smoke test for the 'different' option to make sure the function runs.
        """
        data_list = [session1, session2, session3]
        num_of_features = 2
        option = 'different'
        mm.subset_important_features(data_list, num_of_features, option)

    @classmethod
    def test_smoke_subset_important_features2(cls):
        """
        Simple smoke test for the 'common' option to make sure the function runs.
        """
        data_list = [session1, session2, session3]
        num_of_features = 2
        option = 'common'
        mm.subset_important_features(data_list, num_of_features, option)

    def test_edge_subset_important_features1(self):
        """
        Edge test to make sure the function throws a ValueError
        when the num_of_features is a string
        """
        data_list = [session1, session2, session3]
        num_of_features = '2'
        option = 'different'

        with self.assertRaises(ValueError):
            mm.subset_important_features(data_list, num_of_features, option)

    def test_edge_subset_important_features2(self):
        """
        Edge test to make sure the function throws a ValueError
        when the option is an integer
        """
        data_list = [session1, session2, session3]
        num_of_features = 3
        option = 3

        with self.assertRaises(ValueError):
            mm.subset_important_features(data_list, num_of_features, option)

    def test_edge_subset_important_features3(self):
        """
        Edge test to make sure the function throws a ValueError
        when the num_of_features is less than 2
        """
        data_list = [session1, session2, session3]
        num_of_features = 1
        option = 'common'

        with self.assertRaises(ValueError):
            mm.subset_important_features(data_list, num_of_features, option)

    # Tests for machine_learning_model

    @classmethod
    def test_smoke_machine_learning_model(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        data_list = [session1, session2, session3]
        ml_model = 'DT'
        mm.machine_learning_model(data_list, ml_model)

    def test_edge_machine_learning_model(self):
        """
        Edge test to make sure the function throws a ValueError
        when the ml_model is an integer
        """
        data_list = [session1, session2, session3]
        ml_model = 1
        with self.assertRaises(ValueError):
            mm.machine_learning_model(data_list, ml_model)

    # Tests for kmean_clustering
    @classmethod
    def test_smoke_kmean_clustering(cls):
        """
        Simple smoke test to make sure the function runs.
        """
        data_list = [session1, session2, session3]
        num_of_sessions = 2
        num_of_clusters = 2
        mm.kmean_clustering(data_list, num_of_sessions, num_of_clusters)

    def test_edge_kmean_clustering1(self):
        """
        Edge test to make sure the function throws a ValueError
        when the num_of_sessions is a string
        """
        data_list = [session1, session2, session3]
        num_of_sessions = 'two'
        num_of_clusters = 2
        with self.assertRaises(ValueError):
            mm.kmean_clustering(data_list, num_of_sessions, num_of_clusters)

    def test_edge_kmean_clustering2(self):
        """
        Edge test to make sure the function throws a ValueError
        when the num_of_sessions is less than 2
        """
        data_list = [session1, session2, session3]
        num_of_sessions = 1
        num_of_clusters = 2
        with self.assertRaises(ValueError):
            mm.kmean_clustering(data_list, num_of_sessions, num_of_clusters)

    def test_edge_kmean_clustering3(self):
        """
        Edge test to make sure the function throws a ValueError
        when the num_of_clusters is a string
        """
        data_list = [session1, session2, session3]
        num_of_sessions = 1
        num_of_clusters = '3'
        with self.assertRaises(ValueError):
            mm.kmean_clustering(data_list, num_of_sessions, num_of_clusters)
