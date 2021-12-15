"""
This module do all the plotting used for visualization, based on
the preprocessing results of graph_data
"""

import altair as alt


def plot_log(data, student, activity, y_option, type='average'):
    """
    plot the histgram of selected activity based on data

    Parameter
    ---------
    data: a dataframe with the same structure as graph_data.session_avg returns
    y_option: a list with data type string and items
              are among the column names of parameter 'data'

    Return
    ---------
    a plot with x-axis lists different sessions,
    y-axis is the log activity with different colors of
    blocks representing the amount that the selected
    log activity spent on different kinds of activities.
    """
    if type == 'student':
        if data.shape == (4169, 10):
            df_selected = data[(data['activity'].isin(activity))
                               & (data['student_id'] == student)]
            base = alt.Chart(df_selected, width=350, height=400)
        else:
            raise ValueError("The input data is not used for \
                             plotting student log graph")
    elif type == 'average':
        if data.shape == (54, 9):
            df_avg_selected = data[(data['activity'].isin(activity))]
            base = alt.Chart(df_avg_selected, width=350, height=400)
        else:
            raise ValueError("The input data is not used for \
                             plotting average log graph")
    else:
        raise ValueError("Type should be either 'student' or 'average'")

    log_p = base.mark_bar().encode(
        x='session:N',
        y=y_option,
        color='activity',
        tooltip=[y_option, 'activity']
        ).interactive()

    return log_p


def plot_mid(avg_data, area_data):
    """
    plot the line chart reflecting changes within different
    sessions of the class average, Q1, Q3 and selected students.

    Parameter
    ---------
    data: a dataframe with the same structure as graph_data.mid_avg returns

    Return
    ---------
    a plot with x-axis lists different sessions, y-axis is the score.
    Different colors represent different statistics of the scores
    or different students.
    """
    if area_data.shape != (10, 3):
        raise ValueError("The second dataset has wrong dimension!")
    area = alt.Chart(
        area_data, width=700, height=500
        ).mark_area(opacity=0.3).encode(
            alt.X('Session'),
            alt.Y('max(Avg_grades):Q'),
            alt.Y2('min(Avg_grades):Q'),
            color=alt.value('#e6bcf5')
            )

    mid_plot = alt.Chart(
        avg_data, width=700, height=500
        ).mark_line(
            point=alt.OverlayMarkDef()
            ).encode(
                x=alt.X('Session'),
                y=alt.Y('Avg_grades', scale=alt.Scale(domain=[0, 6]),
                        title='Intermediate Grades'),
                color='Student Id:N',
                strokeDash=alt.condition(
                    alt.datum['Student Id'] == 'Average',
                    alt.value([6, 8]),
                    alt.value([0])
                    ),
                tooltip=['Avg_grades']
                ).interactive().properties(
                    title={'text':
                           "Class and student's average session grades",
                           "subtitle":
                           ["Comparsion between students' session grades and class average grades.",
                            "The shaded area: scores above 20% and below 80% of students scores"]})

    mid_plot = mid_plot + area

    m_conf = mid_plot.configure_title(
        fontSize=24,
        font="Optima",
        color='#9e2a2b',
        subtitleColor='#9e2a2b',
        subtitleFontSize=16,
        anchor="start",
        align="left")

    return m_conf


def plot_mid_hist(session, student, data_for_hist, data_summary):
    """
    This function plots a histgram based on the
    intermediate grades of selected session and students.
    The quartile and mean will also be plotted.

    Parameter
    ---------
    session: selected session from session 1 to session 6
    student: only one selected student from student1 to student 115
    data_for_hist: a dataframe containing the grades only for
                   the selected session, with two columns
                   recording student ID and their grades.
    data_summary: a dataframe containing the some statistics
                  for the selected session's grades including
                  mean, quartiles. It has several columns used
                  for plotting different layers.

    Return
    ---------
    a histgram composed of three layers to display not only
    the grades distribution but also several basic
    statistics of the grades. The grades for selected
    students can also be displayed for a direct comparison.

    """
    if data_for_hist.shape[1] != 2:
        raise ValueError("the first data has wrong number of columns.")
    else:
        pass
    if data_summary.shape[1] != 8:
        raise ValueError("the second data has wrong number of columns.")
    else:
        pass
    mean = data_summary.loc[0, "Session"]
    q_1 = data_summary.loc[1, "Session"]
    median = data_summary.loc[2, "Session"]
    q_3 = data_summary.loc[3, "Session"]

    c_cp = ["#335C67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e",
            "#82e2e9", "a9b7ee", "#cce6f8", "ead4f3", "d5baa7"]
    c_chart_width = 700
    c_chart_height = 400

    layer_chart = (
        alt.Chart(data_for_hist)
        .mark_bar(color=c_cp[session-2])
        .encode(
            alt.X(
                "Session_:Q",
                title="intermediate grades of Session "+str(session),
                bin=alt.Bin(step=0.5)
            ),
            y="count()"
        )
        .properties(
            title={
                "text": "Distribution of intermediate grades of Session " +
                        str(session),
                "subtitle": ["According to the Intermediate data, students score " +
                             str(mean)+" points, on average.",
                             " The median score of the class is " + str(median) +
                             ". For 25 percent students earn a score of more than "+str(q_3)+". ",
                             " counting those who haven't take the intermediate, 25 percent of students score less than "+str(q_1)]
            },
            width=c_chart_width,
            height=c_chart_height
        )
    )

    # create structure rules
    layer_graphical = (
        alt.Chart(data_summary)
        .mark_rule(
            color=c_cp[session+2],
            size=3
        )
        .encode(
            # color = "color:O",
            x=alt.X("Session_:Q",
                    scale=alt.Scale(domain=(0, data_for_hist.loc[:, "Session_"].max())))
        )
        .properties(
            width=c_chart_width,
            height=c_chart_height
        )
    )

    layer_text = (
        alt.Chart(data_summary)
        .mark_text(
            lineBreak="\n",
            dy=-40,
            y=10,
            fontSize=10, fontWeight="bold"
        )
        .encode(
            # text = "labelValue:N",
            text="labelValueLineBreak:N",
            x=alt.X("Session_:Q",
                    scale=alt.Scale(domain=(0, data_for_hist.loc[:, "Session_"].max())))
        )
        .properties(
            width=c_chart_width,
            height=c_chart_height
        )
    )

    chart_hist = layer_chart + layer_graphical + layer_text
    chart_hist_conf = chart_hist.configure_title(
        fontSize=24,
        font="Optima",
        color=c_cp[4],
        subtitleColor=c_cp[4],
        subtitleFontSize=16,
        anchor="start",
        align="left"
    )

    return chart_hist_conf
