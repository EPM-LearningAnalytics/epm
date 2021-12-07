"""
"""
import pandas as pd


def session_agg():
    """
    """
    log_raw = pd.read_csv('EPM_dataset/Data/all_log.csv')
    # drop irrelevant cols
    drop_cols = ['start_time','exercise','end_time']
    log_raw = log_raw.drop(columns = drop_cols)

    log_session = log_raw.groupby(['session','student_id','activity']).sum()
    log_session = log_session.reset_index()

    return log_session

def session_avg():
    """
    """
    log_session = session_agg()
    class_average = log_session.groupby(['session','activity']).mean()
    class_average = class_average.reset_index().drop(columns='student_id')

    return class_average

def mid_avg():
    """
    """
    mid_grades = pd.read_excel('EPM_dataset/Data/intermediate_grades.xlsx',
                                engine='openpyxl')
    mid_avg = pd.DataFrame(mid_grades.mean(axis=0))
    mid_avg = mid_avg.drop(['Student Id'])
    mid_avg.reset_index(inplace = True)
    mid_avg.columns = ['Session', 'Avg_grades']
    mid_avg.insert(0, "Student Id", 'Average')

    mid_std = pd.melt(mid_grades, id_vars='Student Id', 
                  value_vars=['Session 2', 'Session 3',
                              'Session 4', 'Session 5',
                              'Session 6'])
    mid_std.columns = ['Student Id', 'Session', 'Avg_grades']

    mid_all = pd.concat([mid_avg, mid_std])
    mid_all['Student Id'] = mid_all['Student Id'].astype(str)
    
    return mid_all