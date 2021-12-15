"""
This module creates a dataframe that represents which sessions a student 
is recommended to review first before the final exam. 
"""
import os
import pandas as pd
import pickle


def review_alert(id, feat_num):
    """
    retrieve data and trained models from pickle files, 
    predict which sessions are to be prioritized for review. 

    Parameter
    ---------
    id: student ID
    feat_num: the number of features to consider 
    when predicting sessions to review

    Return
    ---------
    a dataframe containing 0 and 1, with rows for regression models
    and columns for sessions. 0 represents the corresponding session 
    is not prioritized to review, while 1 refers to the review priority. 
    """
    if id == '' or feat_num == '':
        raise TypeError("'id' and 'feat_num' should be provided.")

    if feat_num not in [3, 4, 5, '3', '4', '5']:
        raise ValueError("'feat_num' should be either 3, 4, or 5.")

    res = []
    models = ['KNN', 'DT', 'RF', 'NB', 'LR', 'SVC']
    columns = ['Session 2', 'Session 3', 'Session 4', 'Session 5', 'Session 6']
    for model_name in models:
        row = [0] * 5
        for session in range(2, 7):           
            data = 'session_' + str(session) + '_featnum_' + str(feat_num)
            data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', 'features_and_outcome', data)
            df = pickle.load(open(data_path, 'rb'))
            features = df.loc[df['ID'] == int(id)].drop(columns=['Y', 'ID'])
            if len(features) == 0:
                continue

            model = str(model_name) + '_session_' + str(session) + '_featnum_' + str(feat_num)
            model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', 'trained_models', model)
            loaded_model = pickle.load(open(model_path, 'rb'))
            row[session-2] = loaded_model.predict(features)[0]
        res.append(row)

    df = pd.DataFrame(res,
                      index=['K-Nearest Neighbors', 'Decision Tree', 'Random Forest', 'Naive Bayes', 'Log Regression', 'Support Vector Classfier'], 
                      columns=columns)
    return df