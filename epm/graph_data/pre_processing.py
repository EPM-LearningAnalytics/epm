import os
import pandas as pd

def read_all():
    # set dir
    os.chdir('EPM_dataset/Data/Processes')
    
    # create empty dataframe for storage
    column_names = ["session", "student_id", "exercise", 
                  "activity",'start_time','end_time',
                 'idle_time','mouse_wheel','mouse_wheel_click','mouse_click_left',
                 'mouse_click_right','mouse_movement','keystroke']
    log_raw = pd.DataFrame(columns = column_names)
    
    # walk through all the session folders
    sessions = ['Session 1', 'Session 2', 'Session 3', 
                'Session 4', 'Session 5', 'Session 6']
    for session in sessions:
        os.chdir('./'+ session)
        for file in os.listdir():
            # read individual student's file
            log = pd.read_csv(file, sep = ",", header=None)
            log.columns = column_names
            # concatenate to the empty dataframe
            log_raw = pd.concat([log_raw, log])
        os.chdir('../')
   
    # Sort and recode values
    log_raw = log_raw.sort_values(by=['session','student_id'])
    log_raw['activity']=log_raw['activity'].replace(regex=[r'TextEditor\w+',r'Deeds\w+', 
                                                           r'Study\w+', r'(?i)FSM_\w+'], 
                         value=['TextEditor','Deeds','Study','FSM'])
    return log_raw


