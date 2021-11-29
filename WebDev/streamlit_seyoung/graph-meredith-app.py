import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.title('EPM Data Exploring')

st.markdown("""
This app displays the log activity of engineering student!
* **Python libraries:** pandas, streamlit, plotly.express
* **Data source:** [UCI EPM Dataset](https://archive.ics.uci.edu/ml/datasets/Educational+Process+Mining+(EPM)%3A+A+Learning+Analytics+Data+Set#).
""")

st.sidebar.header('User Input Features')

# --- read in dataframe ---
df = pd.read_csv('../../EPM_dataset/Data/log_session_mere.csv')
df_avg = pd.read_csv('../../EPM_dataset/Data/class_avg_mere.csv')


# --- Sidebar - Student Slider ---
student = st.sidebar.slider('Which student?', 1, 115)


# --- Selectbox - log activity selection ---
log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 'mouse_wheel_click',
                'mouse_click_right','mouse_movement','keystroke']
option = st.sidebar.selectbox(
    'Which log activity you like to focus on?',
    log_activity)


# --- Sidebar - Activity selection ---
sorted_activity_unique = sorted( df['activity'].unique() )

selected_activity = st.sidebar.multiselect('Activity', 
                                           sorted_activity_unique, 
                                           sorted_activity_unique)


# --- Filtering data ---
df_selected = df[ (df['activity'].isin(selected_activity)) & (df['student_id'] == student) ]
df_avg_selected = df_avg[ (df['activity'].isin(selected_activity)) ]


# --- Display dataframe ---
st.header('Display Selected Stduents')
st.write('### The student you selected:', 'student '+ str(student))
st.write('Data Dimension: ' + str(df_selected.shape[0]) + ' rows and ' + str(df_selected.shape[1]) + ' columns.')
st.dataframe(df_selected.drop(df_selected.columns[[0, 1, 2]], axis=1))


# --- Class Average Plot ---
# fig_avg = px.bar(df_avg_selected, x='session', y=option,
#                  color='activity', barmode='stack',
#                  color_discrete_sequence=px.colors.qualitative.Set3,
#                  title=(option + ' ' + 'Class Average'))

p = alt.Chart(df_avg_selected, width=350, height=400).mark_bar().encode(
    x='session:N',
    y=option,
    color='activity',
    tooltip=[option, 'activity']
).interactive(
).properties(
    title='Class Average'
)


# --- Student Activity Distribution Plot---
# fig_stu = px.bar(df_selected, x='session', y=option,
#             color='activity', barmode='stack',
#             color_discrete_sequence=px.colors.qualitative.Set3,
#             title=('Student' + ' ' + str(student) + ' ' + option))

s = alt.Chart(df_selected, width=350, height=400).mark_bar().encode(
    x='session:N',
    y=option,
    color='activity',
    tooltip=[option, 'activity']
).interactive(
).properties(
    title='Student' + ' ' + str(student) + ' ' + option
)

x = alt.hconcat(
    p, s
).resolve_scale(
    y='shared'
)

st.write('### The log activity you selected:', option)
st.write(x)

# st.plotly_chart(fig_avg, use_container_width=False)
# st.plotly_chart(fig_stu, use_container_width=False)