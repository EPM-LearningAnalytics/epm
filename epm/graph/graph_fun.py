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

def plot_mid_hist(session, student, data_for_hist, data_summary):
    """
    """
    mean=data_summary.loc[ 0 ,"Session"]
    Q1=data_summary.loc[ 1 ,"Session"]
    median=data_summary.loc[ 2 ,"Session"]
    Q3=data_summary.loc[ 3 ,"Session"]

    c_cp = ["#335C67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e"
        , "#82e2e9", "a9b7ee", "#cce6f8", "ead4f3", "d5baa7"]
    c_chart_width = 700 
    c_chart_height = 400

    layer_chart = (
        alt.Chart(data_for_hist)
        .mark_bar(color = c_cp[session-2])
        .encode(
            alt.X(
                "Session_:Q",
                title = "intermediate grades of Session "+str(session),
                bin = alt.Bin(step = 0.5)
            ),
            y = "count()",
        )
        .properties(
            title = {
                "text": "Distribution of intermediate grades of Session "+str(session),
                "subtitle": ["According to the Intermediate data, students score "+str(mean)+" points, on average."
                            ," The median score of the class is "+str(median)+". For 25 percent students earn a score of more than "+str(Q3)+". "
                            , " counting those who haven't take the intermediate, 25 persent of students score less than "+str(Q1)]
            },
            width = c_chart_width,
            height = c_chart_height
        )
    )

    # create structure rules
    layer_graphical = (
        alt.Chart(data_summary)
        .mark_rule(
            color = c_cp[session+2],
            size = 3
        )
        .encode(
            #color = "color:O",
            x = alt.X("Session_:Q", scale = alt.Scale(domain = (0, data_for_hist.loc[:,"Session_"].max())))
        )
        .properties(
            width = c_chart_width,
            height = c_chart_height
        )
    )

    layer_text = (
        alt.Chart(data_summary)
        .mark_text(
            lineBreak = "\n",
            dy = -40,
            y = 10,
            fontSize = 10, fontWeight = "bold"
        )
        .encode(
            #text = "labelValue:N",
            text = "labelValueLineBreak:N",
            x = alt.X("Session_:Q", scale = alt.Scale(domain = (0, data_for_hist.loc[:,"Session_"].max())))
        )
        .properties(
            width = c_chart_width,
            height = c_chart_height
        )
    )

    chart_hist = layer_chart + layer_graphical + layer_text
    chart_hist_conf = chart_hist.configure_title(
        fontSize = 24,
        font = "Optima",
        color = c_cp[4],
        subtitleColor = c_cp[4],
        subtitleFontSize = 16,
        anchor = "start",
        align = "left"
    )

    return chart_hist_conf

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

