"""
This is a streamlit file used for testing visualizations
"""

import streamlit as st
import pandas as pd
import altair as alt

from epm.graph import *

st.title('EPM Data Exploring')

st.write('This app displays the log activity of engineering student!')

# # --- read in dataframe --
# df = session_agg()
# df_avg = session_avg(df)


# # --- Slider - Student Slider ---
# student = st.slider('1. Which student?', 1, 115)

# # --- Selectbox - log activity selection ---
# log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 'mouse_wheel_click',
#             'mouse_click_right','mouse_movement','keystroke']
# option = st.selectbox(
# '2. Which log activity you like to focus on?',
# log_activity)

# # --- Multiselect - Activity selection ---
# sorted_activity_unique = sorted( df['activity'].unique() )
# selected_activity = st.multiselect('3. Which activity do you want to include', 
#                                         sorted_activity_unique,
#                                         sorted_activity_unique)

# # --- Filtering data ---
# df_selected = df[ (df['activity'].isin(selected_activity)) & (df['student_id'] == student) ]
# df_avg_selected = df_avg[ (df['activity'].isin(selected_activity)) ]

# # --- Class Average Plot ---
# p = plot_log(df_avg_selected, option).properties(
#     title = 'Class Average'
#     )


# # --- Student Activity Distribution Plot---

# s = plot_log(df_selected, option).properties(
#     title='Student' + ' ' + str(student) + ' ' + option
#     )

# # --- Present graphs side by side ---
# x = alt.hconcat(
#     p, s
# ).resolve_scale(
#     y='shared'
# )

# st.write('**Plot Result**: You select ' + 'student ' + str(student) + ' and ' + option)
# st.write(x)


# --- session grades plot ---
mid_all = mid_avg()
students = mid_all['Student Id'].unique()
selected_students = st.multiselect('Students you selected', 
                                        students,
                                        ['Average', 'Q1', 'Q2', 'Q3'])
mid_all = mid_all[mid_all['Student Id'].isin(selected_students)]

m = plot_mid(mid_all)

st.write(m)

# # --- Final grades plot ---
# final_all = final_step_1()
# final_all = final_avg(final_all)
# students_final = final_all['Student ID'].unique()
# selected_students_final = st.multiselect('Students you selected', 
#                                         students_final,
#                                         ['Average', 'Q1', 'Q2', 'Q3'])
# final_all = final_all[final_all['Student ID'].isin(selected_students_final)]

# m_final = plot_final(final_all)

# st.write(m_final)


# --- intermediate grades ---

# data = pd.read_excel('data/intermediate_grades.xlsx',engine='openpyxl')
# Student = 1
# Session = 2

# data_for_hist = data[['Student Id','Session '+str(Session)]]
# data_for_hist.columns = ['Student_Id','Session_']

# data_summary = (
#     data_for_hist
#     .describe()
#     .reset_index()
#     .query("index == 'mean' | index == '25%' | index == '50%' | index == '75%'")
#     .assign(Session = lambda x: x.Session_.round(1))
# )

# data_summary = data_summary.append({'index': 1, 
#                                     'Student_Id':Student, 
#                                     'Session_':data_for_hist.loc[ Student-1 ,"Session_"], 
#                                     'Session':data_for_hist.loc[ Student-1 ,"Session_"]}, ignore_index=True)

# data_summary['Session'] = data_summary['Session'].astype("str")

# c_cp = ["#335C67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e"
#         , "#82e2e9", "a9b7ee", "#cce6f8", "ead4f3", "d5baa7"]
# c_chart_width = 600 
# c_chart_height = 250

# data_summary = (
#     data_summary
#     .assign(label = ["Mean", "Q1", "Median", "Q3", "student "+str(Student)])
#     .assign(color = [c_cp[2], c_cp[3], c_cp[4], c_cp[2], c_cp[3]])
#     .assign(labelValue = lambda x: x.label + " " + x.Session)
#     .assign(labelValueLineBreak = lambda x: x.label + "\n" + x.Session))

# mean=data_summary.loc[ 0 ,"Session"]
# Q1=data_summary.loc[ 1 ,"Session"]
# median=data_summary.loc[ 2 ,"Session"]
# Q3=data_summary.loc[ 3 ,"Session"]


# layer_chart = (
#     alt.Chart(data_for_hist)
#     .mark_bar(color = c_cp[Session-2])
#     .encode(
#         alt.X(
#             "Session_:Q",
#             title = "intermediate grades of Session "+str(Session),
#             bin = alt.Bin(step = 0.5)
#         ),
#         y = "count()",
#     )
#     .properties(
#         title = {
#             "text": "Distribution of intermediate grades of Session "+str(Session),
#             "subtitle": ["According to the Intermediate data, students score "+str(mean)+" points, on average."
#                          ," The median score of the class is "+str(median)+". For 25 percent students earn a score of more than "+str(Q3)+". "
#                          , " counting those who haven't take the intermediate, 25 persent of students score less than "+str(Q1)]
#         },
#         width = c_chart_width,
#         height = c_chart_height
#     )
# )

# # create structure rules
# layer_graphical = (
#     alt.Chart(data_summary)
#     .mark_rule(
#         color = c_cp[Session+2],
#         size = 3
#     )
#     .encode(
#         #color = "color:O",
#         x = alt.X("Session_:Q", scale = alt.Scale(domain = (0, data_for_hist.loc[:,"Session_"].max())))
#     )
#     .properties(
#         width = c_chart_width,
#         height = c_chart_height
#     )
# )

# layer_text = (
#     alt.Chart(data_summary)
#     .mark_text(
#         lineBreak = "\n",
#         dy = -40,
#         y = 10,
#         fontSize = 10, fontWeight = "bold"
#     )
#     .encode(
#         #text = "labelValue:N",
#         text = "labelValueLineBreak:N",
#         x = alt.X("Session_:Q", scale = alt.Scale(domain = (0, data_for_hist.loc[:,"Session_"].max())))
#     )
#     .properties(
#         width = c_chart_width,
#         height = c_chart_height
#     )
# )

# chart_hist = layer_chart + layer_graphical + layer_text
# chart_hist_conf = chart_hist.configure_title(
#     fontSize = 24,
#     font = "Optima",
#     color = c_cp[4],
#     subtitleColor = c_cp[4],
#     subtitleFontSize = 16,
#     anchor = "start",
#     align = "left"
# )


# chart_hist_conf
# --- Slider - Student Slider ---
student = st.slider('Which student?', 1, 115)

# --- Slider - Session Slider ---
session = st.slider('Which session?', 2, 6)

data_for_hist = mid_hist(student, session)
data_summary = mid_summary(student, data_for_hist)

p = plot_mid_hist(session, student, data_for_hist, data_summary)

st.write(p)