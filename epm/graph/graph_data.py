"""
This module prepares epm datasets in 'data' folder for plotting.
"""
import pandas as pd


def session_agg():
    """
    This function automatically reads csv file contains
    all the detailed students' log activities across six sessions.
    Then it generates the sum of each students' log activities
    for each activity type of one session for six sessions

    Return
    -------
    A dataframe with 4169 rows and 10 columns
    showing aggregated log activities for each activity type
    for each student in six sessions

    """
    log_raw = pd.read_csv('data/all_log.csv')
    # drop irrelevant cols
    drop_cols = ['start_time', 'exercise', 'end_time']
    log_raw = log_raw.drop(columns=drop_cols)

    log_session = log_raw.groupby(['session', 'student_id', 'activity']).sum()
    log_session = log_session.reset_index()

    return log_session


def session_avg(log_session):
    """
    This function read calculates the mean of
    log activities across six sessions.

    Parameter
    ---------
    log_session: DataFrame
        Dataframe generated by session_agg function

    Return
    ------
    A dataframe with 54 rows and 9 columns

    """
    if not isinstance(log_session, pd.DataFrame):
        raise ValueError("input is not a dataframe")
    else:
        pass
    if log_session.shape[1] != 10:
        raise ValueError("columns' number doesn't satisfy the demand")
    else:
        pass
    class_average = log_session.groupby(['session', 'activity']).mean()
    class_average = class_average.reset_index().drop(columns='student_id')

    return class_average


def mid_avg():
    """
    This function automatically reads in the intermediate grades data in
    the "data" folder, then calculates out the quantile and average grades
    of the class for each session.

    Return
    ---------
    The function returns two dataframe of three columns,
    which are 'Student Id', 'Session', 'Avg_grades'.
    One includes the average score and all the students'
    score, which is used to plot the line chart of the select data.
    The other includes the data of 20% and 80% quartiles,
    which is used to plot the shaded part.

    """
    mid_grades = pd.read_excel('data/intermediate_grades.xlsx',
                               engine='openpyxl')
    # calculate the mean
    mid_avg = pd.DataFrame(mid_grades.mean(axis=0))
    mid_avg = mid_avg.drop(['Student Id'])
    mid_avg.reset_index(inplace=True)
    mid_avg.columns = ['Session', 'Avg_grades']
    mid_avg.insert(0, "Student Id", 'Average')

    # calculate the Q1
    mid_avg_q1 = pd.DataFrame(mid_grades.quantile(q=0.20, axis=0))
    mid_avg_q1 = mid_avg_q1.drop(['Student Id'])
    mid_avg_q1.reset_index(inplace=True)
    mid_avg_q1.columns = ['Session', 'Avg_grades']
    mid_avg_q1.insert(0, "Student Id", 'Q1')

    # calculate the Q3
    mid_avg_q3 = pd.DataFrame(mid_grades.quantile(q=0.80, axis=0))
    mid_avg_q3 = mid_avg_q3.drop(['Student Id'])
    mid_avg_q3.reset_index(inplace=True)
    mid_avg_q3.columns = ['Session', 'Avg_grades']
    mid_avg_q3.insert(0, "Student Id", 'Q3')

    # transform the data into another dataframe
    mid_std = pd.melt(mid_grades, id_vars='Student Id',
                      value_vars=['Session 2', 'Session 3', 'Session 4',
                                  'Session 5', 'Session 6'])
    mid_std.columns = ['Student Id', 'Session', 'Avg_grades']

    # mid_all = pd.concat([mid_avg, mid_avg_q1,
    # mid_avg_q3, mid_std])
    mid_all = pd.concat([mid_avg, mid_std])
    mid_all['Student Id'] = mid_all['Student Id'].astype(str)
    # cut the long tail after the dot
    mid_all['Avg_grades'] = mid_all.apply(lambda x: round(x["Avg_grades"],
                                                          2), axis=1)

    mid_area = pd.concat([mid_avg_q1, mid_avg_q3])
    mid_area['Avg_grades'] = mid_area.apply(lambda x: round(x["Avg_grades"],
                                                            2), axis=1)

    return mid_all, mid_area


def mid_hist(session):
    """
    This function grab and construct a dataframe only
    contains the grades for the selected session
    in intermediate grades.

    Parameter
    ---------
    session: which session the user select.

    Return
    ---------
    a dataframe of the grades for the selected session,
    with columns get renamed for the convenience of
    next step's data preprocessing.

    """
    if not isinstance(session, int):
        raise ValueError("The input data is not of type int")
    else:
        pass
    if session not in list((2, 3, 4, 5, 6)):
        raise ValueError("The input number cannot refer to a session")
    else:
        pass
    data = pd.read_excel('data/intermediate_grades.xlsx', engine='openpyxl')

    data_for_hist = data[['Student Id', 'Session '+str(session)]]
    data_for_hist.columns = ['Student_Id', 'Session_']

    return data_for_hist


def mid_summary(student, data_for_hist):
    """
    This function calculates out several statistics
    (including mean and quartiles) and return them in
    a dataframe with several columns used as the
    preparation for the plotting function plot_mid_hist.

    Parameter
    ---------
    student: the only one selected student from the whole class.
    data_for_hist: the output of the former function mid_hist, a dataframe
                   of the grades in the selected session.

    Return
    ---------
    The function returns a dataframe to display
    some statistics(including the mean, quartiles)
    for the selected session's grades.
    As this function is used for the preprocessing
    of plottinghistgram in function plot_mid_hist,
    the output contains several columns that looks unnecessary
    but useful when plotting the several layers.

    """
    if not isinstance(student, int):
        raise ValueError("The first parameter input is not of type int")
    else:
        pass
    if not isinstance(data_for_hist, pd.DataFrame):
        raise ValueError("The second parameter input is not of type dataframe")
    else:
        pass
    if data_for_hist.shape[1] != 2:
        raise ValueError("Column number is not right")
    else:
        pass
    if student not in data_for_hist['Student_Id']:
        raise ValueError("Cannot find the input student id")
    else:
        pass
    data_summary = (
        data_for_hist
        .describe()
        .reset_index()
        .query("index == 'mean' | index == '25%' | \
        index == '50%' | index == '75%'")
        .assign(Session=lambda x: x.Session_.round(1))
    )

    data_summary = data_summary.append({'index': 1,
                                        'Student_Id': student,
                                        'Session_':
                                        data_for_hist.loc[student-1,
                                                          "Session_"],
                                        'Session':
                                        data_for_hist.loc[student-1,
                                                          "Session_"]},
                                       ignore_index=True)

    data_summary['Session'] = data_summary['Session'].astype("str")

    c_cp = ["#335C67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e",
            "#82e2e9", "a9b7ee", "#cce6f8", "ead4f3", "d5baa7"]

    data_summary = (
        data_summary
        .assign(label=["Mean", "Q1", "Median", "Q3", "student "+str(student)])
        .assign(color=[c_cp[2], c_cp[3], c_cp[4], c_cp[2], c_cp[3]])
        .assign(labelValue=lambda x: x.label + " " + x.Session)
        .assign(labelValueLineBreak=lambda x: x.label + "\n" + x.Session))

    return data_summary
