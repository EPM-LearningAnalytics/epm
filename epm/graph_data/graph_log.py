import os
import pandas as pd


def session_agg():
    log_raw = pd.read_csv('EPM_dataset/Data/all_log.csv')
    # drop irrelevant cols
    drop_cols = ['start_time','exercise','end_time']
    log_raw = log_raw.drop(columns = drop_cols)

    log_session = log_raw.groupby(['session','student_id','activity']).sum()
    log_session = log_session.reset_index()

    return log_session

def session_avg():
    
    log_session = session_agg()
    class_average = log_session.groupby(['session','activity']).mean()
    class_average = class_average.reset_index().drop(columns='student_id')

    return class_average

