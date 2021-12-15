#!/usr/bin/env python
# coding: utf-8

"""
This module preprocess the log activity data
"""


# load libraries
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler


def read_file(file_dir='../../data/Processes'):
    """
    Read log files from given directory

    Parameters
    ----------
    file_dir: Local path of EPM Processes files

    Return
    ----------
    A list containing pandas dataframes of all sessions' raw data
    """
    sessions = []
    for root, dirs, files in os.walk(file_dir, topdown=False):
        if files:
            session = []
            for file in files:
                if file != '.DS_Store':
                    path = os.path.join(root, file)
                    log = pd.read_csv(path, sep=",", header=None)
                    session.append(log)
            if session:
                session_pd = pd.concat(session)
                session_pd.columns = ["session", "student_id", "exercise", 
                            "activity",'start_time','end_time',
                            'idle_time','mouse_wheel','mouse_wheel_click','mouse_click_left',
                            'mouse_click_right','mouse_movement','keystroke']
                sessions.append(session_pd)
    
    # Insert the ordered session data to the data_list array.
    data_list = [0]*7
    session_num = 0
    while sessions:
        session_num = int(sessions[0]['session'].unique())
        data_list[session_num] = sessions.pop(0)
        session_num +=1

    # confirm
    for i, session in enumerate(data_list):
        if i == 0: continue
        session_num = session['session'].unique()[0]
        print(f"{i}th element in the sessions list represents Session{session_num}")
    
    return data_list



def feature_manipulation(data_list):
    """
    Transform raw log data to cleaned and formatted data

    Parameters
    ----------
    data_list: A list containing pandas dataframes of all sessions' raw data

    Return
    ----------
    A list containing pandas dataframes of all sessions' cleaned and formatted data
    """
    # Error meassage
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    # Drop irrelevant columns and give simpler column names
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        data_list[i] = session.drop(columns=['session', 'exercise', 'start_time', 'end_time'])
        data_list[i].columns = ["ID", "ACT",
                                'DUR', 'MW', 'MWC', 'MCL',
                                'MCR', 'MM', 'KS']
    # Rename the values
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        session['ACT'] = session['ACT'].replace(regex=['TextEditor\w+', 'Deeds\w+',
                                                       'Study\w+', '(?i)FSM_\w+'],
                                                value=['TextEditor', 'Deeds', 'Study', 'FSM'])
        session['ACT'] = session['ACT'].str.strip()
    # Sum figures for each features of each student
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        data_list[i] = session.groupby(['ID', 'ACT']).sum()
    # Transform variables from two dimensions to one
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        data_list[i] = session.pivot_table(index=['ID'],
                                           columns='ACT',
                                           values=['DUR', 'MW', 'MWC',
                                                   'MCR', 'MCL', 'MM', 'KS'])
        data_list[i].columns = ['_'.join(col) for col in data_list[i].columns.values]
    # Replace nan to 0
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        data_list[i] = session.fillna(0)
    return data_list


def feature_standardization(data_list):
    """
    Standardize features in log data

    Parameters
    ----------
    data_list: A list containing pandas dataframes of all sessions' data

    Return
    ----------
    A list containing pandas dataframes of all sessions' cleaned and formatted data
    """
    # Error meassage
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    # Standardize features
    standardized_features = []
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        numerical = session.select_dtypes(include='float64').columns
        # This will transform the selected columns and merge to the original data frame
        session.loc[:, numerical] = StandardScaler().fit_transform(session.loc[:, numerical])
        standardized_features.append(session)
    return standardized_features


def merge_all_data(data_list, grades):
    """
    Merge log data from all sessions and grades

    Parameters
    ----------
    datalist: A list containing pandas dataframes of all sessions' raw data
    grades: A panda dataframe with all grades

    return
    ----------
    A list containing pandas dataframes of all sessions' raw data
    """
    # Error meassages
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    if not isinstance(grades, pd.DataFrame) is True:
        raise ValueError("'grades' should be a panda dataframe.")
    # Merge all datasets
    for i, features in enumerate(data_list):
        if i == 0:
            continue
        data_list[i] = features.merge(grades[['ID', 'MID' + str(i+1), 'RES' + str(i+1)]],
                                      how='inner', on='ID')
        data_list[i] = data_list[i].rename(columns={'RES' + str(i+1): 'Y'})
    return data_list


def save_data(data_list, save_dir='../../data/'):
    """
    Save processed data to csv files

    Parameters
    ----------
    datalist: A list containing pandas dataframes of all sessions' raw data
    save_dir: A path to save files in

    return
    ----------
    Show the result of saving grades, "Saved"
    """
    # Error meassage
    if not isinstance(data_list, list) is True:
        raise ValueError("'data_list' should be a list including panda dataframes.")
    # Save datasets
    for i, session in enumerate(data_list):
        if i == 0:
            continue
        file_name = "variables_session_" + str(i) + "_not_filtered.csv"
        session.to_csv(save_dir + file_name)
    return print("Saved")
