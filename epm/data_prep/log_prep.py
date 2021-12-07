#!/usr/bin/env python
# coding: utf-8

"""
This module preprocess the log activity data
"""


# load libraries
import os
import glob
import pandas as pd
import numpy as np


def read_file(file_dir = '/UW/EPM_Project/EPM_dataset/Data/Processes'):
    sessions = []
    for root, dirs, files in os.walk(file_dir, topdown=False):
        if files:
            session = []
            for file in files:
                path = os.path.join(root, file)
                log = pd.read_csv(path, sep=",", header=None)
                session.append(log)

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
        if i == 0:continue
        session_num = session['session'].unique()[0]
        print(f"{i}th element in the sessions list represents Session{session_num}")
    
    return data_list

def feature_manipulation(data_list):

    # drop irrelevant columns and give simpler column names
    for i, session in enumerate(data_list):
        if i == 0: continue
        data_list[i] = session.drop(columns = ['session', 'exercise', 'start_time', 'end_time'])
        data_list[i].columns = ["ID", "ACT",
                                'DUR','MW','MWC','MCL',
                                'MCR','MM','KS']

    # recname the values 
    for i, session in enumerate(data_list):
        if i == 0: continue
        session['ACT'] = session['ACT'].replace(regex=['TextEditor\w+','Deeds\w+', 'Study\w+', '(?i)FSM_\w+'], 
                             value=['TextEditor','Deeds','Study','FSM'])
        session['ACT'] = session['ACT'].str.strip()
    
    # sum figures for each features of each student
    for i, session in enumerate(data_list):
        if i == 0: continue
        data_list[i] = session.groupby(['ID','ACT']).sum()
   
    # transform variables from two dimensions to one
    for i, session in enumerate(data_list):
        if i == 0: 
            continue
        data_list[i] = session.pivot_table(index = ['ID'],
                                           columns = 'ACT',
                                           values = ['DUR', 'MW', 'MWC', 'MCR', 'MCL', 'MM', 'KS'])
        data_list[i].columns = ['_'.join(col) for col in data_list[i].columns.values]
       
    # replace nan to 0
    for i, session in enumerate(data_list):
        if i == 0: continue
        data_list[i] = session.fillna(0)


    return data_list

def save_data(data_list,save_dir = '~/UW/CSE583/Explore/data/'):
    """ 
    save to csv
    """
    for i, session in enumerate(data_list):
        if i == 0: continue
        file_name = "variables_session_" + str(i) + "_not_filtered.csv"
        session.to_csv(save_dir+ file_name)
    return 0
            

        
def main():
    A = read_file()
    A = feature_manipulation(A)
    save_data(A)
    return 0


if __name__ == '__main__':
    main()