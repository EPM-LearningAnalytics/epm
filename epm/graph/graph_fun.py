"""
This module do all the plotting used for visualization, based on 
the preprocessing results of graph_data
"""

import altair as alt

def plot_log(data, y_option):
    """
    plot the histgram of selected activity based on data

    Parameter
    ---------
    data: a dataframe with the same structure as graph_data.session_avg returns
    y_option: a list with data type string and items are among the column names of parameter 'data'

    Return
    ---------
    a plot with x-axis lists different sessions, y-axis is the log activity with different colors of
    blocks representing the amount that the selected log activity spent on different kinds of activities.
    """
    p = alt.Chart(data, width=350, height=400).mark_bar().encode(
        x='session:N',
        y=y_option,
        color='activity',
        tooltip=[y_option, 'activity']
        ).interactive()
    
    return p

def plot_mid(data):
    """
    plot the line chart reflecting changes within different sessions of the class average, Q1, Q2, Q3
    and selected students.

    Parameter
    ---------
    data: a dataframe with the same structure as graph_data.mid_avg returns

    Return
    ---------
    a plot with x-axis lists different sessions, y-axis is the score. Different colors represent different
    statistics of the scores or different students.
    """
    m = alt.Chart(data, width=700, height=500
    ).mark_line(
    ).encode(
        x='Session', 
        y='Avg_grades',
        color = 'Student Id:N',
        tooltip=['Avg_grades']
    ).interactive().properties(
    title = "Class and student's average session grades")

    return m

def plot_final(data):
    """
    plot the line chart reflecting changes within different sessions of the class average, Q1, Q2, Q3
    and selected students. Data is based on the final. This function works quite similarly to the plot_mid
    but is designated for plotting the results of the final.

    Parameter
    ---------
    data: a dataframe with the same structure as graph_data.final_avg returns

    Return
    ---------
    a plot with x-axis lists different sessions, y-axis is the score. Different colors represent different
    statistics of the scores or different students. 
    """
    m = alt.Chart(data, width=700, height=500
        ).mark_line(point = True
        ).encode(
            x='Session', 
            y='Avg_grades',
            color = 'Student ID:N',
            tooltip=['Avg_grades']
        ).interactive().properties(
        title = "Comparison of class and student's final grades on a standard scale")
    return(m)
