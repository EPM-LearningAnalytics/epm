#!/usr/bin/env python

# coding: utf-8

"""
This module subsets the certain number of important features
and detects student behavior and grouping students
"""

# Load libraries
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans


def subset_important_features(data_list, num_of_features, option):
    """
    Subset the certain number of statistically significant features

    Parameters
    ----------
    data_list: A list containing pandas dataframes
               including sessions' and grades' data
    num_of_features: The number of features that a user wants to subset
    option: Different ways to subset the data_list
            'common': Subset common significant features across all sessions
            'different': Subset significant features from each session

    Return
    ----------
    A list containing subsetted pandas dataframes
    """
    if not isinstance(num_of_features, int) is True:
        raise ValueError("'num_of_features' should be an integer.")
    if not isinstance(option, str) is True:
        raise ValueError("'option' should be a string ('common' or 'different').")
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    if not num_of_features >= 2:
        raise ValueError("'num_of_features' should be greater than 2.")
    else:
        # Subset common significant features across all sessions
        if option == 'different':
            important_features = []
            for i, session in enumerate(data_list):
                if i == 0:
                    continue
                ivs = session.drop(columns=['ID', 'Y'])
                outcome = session['Y']
                clf = ExtraTreesClassifier(n_estimators=50)
                clf = clf.fit(ivs, outcome)
                feat_importances = pd.Series(clf.feature_importances_, index=ivs.columns)
                features = feat_importances.nlargest(num_of_features).index[0:num_of_features]
                important_features.append(pd.DataFrame(features, columns=['session' + str(i+1)]))
                important_features[i-1].loc[num_of_features] = ['Y']
                important_features[i-1].loc[num_of_features+1] = ['ID']
            for i, session in enumerate(data_list):
                if i == 0:
                    continue
                data_list[i] = session[important_features[i-1]['session'+str(i+1)]]
            return data_list

        # Subset significant features from each session
        elif option == 'common':
            num = 0
            j = 10
            while num < num_of_features-1:
                important_features = []
                for i, session in enumerate(data_list):
                    if i == 0:
                        continue
                    ivs = session.drop(columns=['ID', 'Y'])
                    outcome = session['Y']
                    clf = ExtraTreesClassifier(n_estimators=50)
                    clf = clf.fit(ivs, outcome)
                    feat_importances = pd.Series(clf.feature_importances_, index=ivs.columns)
                    features = feat_importances.nlargest(j).index[0:j]
                    important_features.append(features)
                common_features = list(set.intersection(*map(set, important_features)))
                num = len(common_features)
                j += 1
            if len(common_features) > num_of_features-1:
                common_features = common_features[0:num_of_features]
                for i, session in enumerate(data_list):
                    if i == 0:
                        continue
                    common_features.append('ID')
                    common_features.append('MID'+str(i+1))
                    data_list[i] = session[common_features]
                    del common_features[-2:]
            if len(common_features) == num_of_features-1:
                for i, session in enumerate(data_list):
                    if i == 0:
                        continue
                    common_features.append('ID')
                    common_features.append('MID'+str(i+1))
                    data_list[i] = session[common_features]
                    del common_features[-2:]
            return data_list


def machine_learning_model(data_list, ml_model):
    """
    Fit a machine learning model

    Parameters
    ----------
    data_list: A list containing pandas dataframes
               including sessions' and grades' data
    ml_model: A machine learning model that a user wants to fit
                'KNN': K-nearest neighbors
                'DT': Decision tree
                'RF': Randome forest
                'NB': Naive Bayes
                'LR': Logistic regression
                'SVC': Support vector classifier

    Return
    ----------
    A list containing pandas dataframes including features
    and a fitted result from a machine learning model
    """
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    if not isinstance(ml_model, str) is True:
        raise ValueError("'ml_model' should be a string.")
    else:
        for i, session in enumerate(data_list):
            if i == 0:
                continue
            ivs = session.drop(columns=['Y'])
            outcome = session['Y']
            # Fit the K-nearest neighbors
            if ml_model == 'KNN':
                cknn = KNeighborsClassifier(n_neighbors=10, metric='minkowski',
                                            p=2).fit(ivs, outcome)
                predict = cknn.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            # Fit the decision tree
            elif ml_model == 'DT':
                cdt = DecisionTreeClassifier(criterion='entropy').fit(ivs, outcome)
                predict = cdt.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            # Fit the random forest
            elif ml_model == 'RF':
                crf = RandomForestClassifier(n_estimators=10, criterion='entropy').fit(ivs, outcome)
                predict = crf.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            # Fit the naive bayes
            elif ml_model == 'NB':
                cnb = GaussianNB().fit(ivs, outcome)
                predict = cnb.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            # Fit the logistic regression
            elif ml_model == 'LR':
                clr = LogisticRegression(solver='liblinear').fit(ivs, outcome)
                predict = clr.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            # Fir the support vector classfier
            elif ml_model == 'SVC':
                csvm = SVC(kernel='rbf', random_state=0).fit(ivs, outcome)
                predict = csvm.predict(ivs)
                session = session.assign(Predicted_Y=predict)
            data_list[i] = session
        return data_list


def kmean_clustering(data_list, num_of_sessions, num_of_clusters):
    """
    Fit the k-means clustering

    Parameters
    ----------
    data_list: A list containing pandas dataframes
               including sessions' and grades' data
    num_of_sessions: The timing when a user wants to form a group
    num_of_clusters: The number of clusters that a user wants to form

    Return
    ----------
    A list containing pandas dataframes including features
    and results from the k-mean clustering
    """
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    if not isinstance(num_of_sessions, int) is True:
        raise ValueError("'num_of_sessions' should be an integer.")
    if not isinstance(num_of_sessions, int) is True:
        raise ValueError("'num_of_clusters' should be an integer.")
    if not num_of_sessions >= 2:
        raise ValueError("'num_of_sessions' should be greater than 2.")
    else:
        new_data_list = [0]*5
        for i in range(0, num_of_sessions):
            if i == 0:
                continue
            # k-mean clustering for the session 2
            if i == 1:
                new_data_list[i-1] = data_list[i]
                kmeans = KMeans(n_clusters=num_of_clusters, init='k-means++',
                                max_iter=300, n_init=10)
                kmeans.fit(new_data_list[i-1].loc[:, new_data_list[i-1].columns != 'ID'])
                y_pred = kmeans.fit_predict(new_data_list[i-1].iloc[:, :])
                new_data_list[i-1] = new_data_list[i-1].assign(group=y_pred)
            # k-mean clustering for the session 3-6
            if 2 <= i <= 5:
                logs = data_list[i].columns[0:len(data_list[i].columns)-2]
                new_data_list[i-1] = new_data_list[i-2].merge(data_list[i], how="outer", on=['ID'])
                # Calculate current intermediate (mid) scores with previous scores
                mid_cols = [col for col in new_data_list[i-1].columns if col.startswith('MID')]
                new_data_list[i-1]['MID_Mean'] = new_data_list[i-1][mid_cols].mean(axis=1)

                j = 0
                all_log_cols = []
                # Calculate current intermediate (mid) log feature(s) with previous log feature(s)
                while j < len(logs):
                    log_cols = [col for col in new_data_list[i-1].columns
                                if col.startswith(logs[j])]
                    all_log_cols.append(logs[j]+'_Mean')
                    new_data_list[i-1][logs[j]+'_Mean'] = new_data_list[i-1][log_cols].mean(axis=1)
                    j += 1
                cols_collection = all_log_cols+['ID', 'MID_Mean']

                new_data_list[i-1] = new_data_list[i-1][cols_collection]
                kmeans = KMeans(n_clusters=num_of_clusters, init='k-means++',
                                max_iter=300, n_init=10)
                data_for_fitting = new_data_list[i-1].loc[:, new_data_list[i-1].columns != 'ID']
                kmeans.fit(data_for_fitting)
                y_pred = kmeans.fit_predict(data_for_fitting)
                new_data_list[i-1] = new_data_list[i-1].assign(group=y_pred)
        return new_data_list[num_of_sessions-2]


def main():
    print('Done!')


if __name__ == '__main__':
    main()
