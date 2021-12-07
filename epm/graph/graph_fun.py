"""
"""

import altair as alt

def plot_log(data, y_option):
    """
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


