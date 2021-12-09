"""
This is a streamlit file used for testing visualizations
"""

import streamlit as st
import pandas as pd
import altair as alt

from epm.graph import *

st.title('EPM Data Exploring')

st.write('This app displays the log activity of engineering student!')

# --- read in dataframe ---
df = session_agg()
df_avg = session_avg(df)


# --- Slider - Student Slider ---
student = st.slider('1. Which student?', 1, 115)

# --- Selectbox - log activity selection ---
log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 'mouse_wheel_click',
            'mouse_click_right','mouse_movement','keystroke']
option = st.selectbox(
'2. Which log activity you like to focus on?',
log_activity)

# --- Multiselect - Activity selection ---
sorted_activity_unique = sorted( df['activity'].unique() )
selected_activity = st.multiselect('3. Which activity do you want to include', 
                                        sorted_activity_unique,
                                        sorted_activity_unique)

# --- Filtering data ---
df_selected = df[ (df['activity'].isin(selected_activity)) & (df['student_id'] == student) ]
df_avg_selected = df_avg[ (df['activity'].isin(selected_activity)) ]

# --- Class Average Plot ---
p = plot_log(df_avg_selected, option).properties(
    title = 'Class Average'
    )


# --- Student Activity Distribution Plot---

s = plot_log(df_selected, option).properties(
    title='Student' + ' ' + str(student) + ' ' + option
    )

# --- Present graphs side by side ---
x = alt.hconcat(
    p, s
).resolve_scale(
    y='shared'
)

st.write('**Plot Result**: You select ' + 'student ' + str(student) + ' and ' + option)
st.write(x)


# --- session grades plot ---
mid_all = mid_avg()
students = mid_all['Student Id'].unique()
selected_students = st.multiselect('Students you selected', 
                                        students,
                                        ['Average', 'Q1', 'Q2', 'Q3'])
mid_all = mid_all[mid_all['Student Id'].isin(selected_students)]

m = plot_mid(mid_all)

st.write(m)

# --- Final grades plot ---
final_all = final_step_1()
final_all = final_avg(final_all)
students_final = final_all['Student ID'].unique()
selected_students_final = st.multiselect('Students you selected', 
                                        students_final,
                                        ['Average', 'Q1', 'Q2', 'Q3'])
final_all = final_all[final_all['Student ID'].isin(selected_students_final)]

m_final = plot_final(final_all)

st.write(m_final)