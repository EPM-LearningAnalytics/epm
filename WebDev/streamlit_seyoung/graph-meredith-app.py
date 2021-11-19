import streamlit as st
import pandas as pd
import plotly.express as px

st.title('EPM Data Exploring')

st.markdown("""
This app displays the log activity of engineering student!
* **Python libraries:** pandas, streamlit, plotly.express
* **Data source:** [UCI EPM Dataset](https://archive.ics.uci.edu/ml/datasets/Educational+Process+Mining+(EPM)%3A+A+Learning+Analytics+Data+Set#).
""")

st.sidebar.header('User Input Features')

# --- read in dataframe ---

df = pd.read_csv('../../EPM_dataset/Data/log_session.csv')

# --- Sidebar - Student Slider ---
student = st.sidebar.slider('Student', 1, 115)


# --- Selectbox - log activity selection ---
log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 'mouse_wheel_click',
                'mouse_click_right','mouse_movement','keystroke']
option = st.sidebar.selectbox(
    'Which log activity you like to focus on?',
    log_activity
)


# --- Sidebar - Activity selection ---
sorted_activity_unique = sorted( df['activity'].unique() )

selected_activity = st.sidebar.multiselect('Activity', sorted_activity_unique, sorted_activity_unique)


# --- Filtering data ---
df_selected = df[ (df['activity'].isin(selected_activity)) & (df['student_id'] == student) ]

# --- Display dataframe ---
st.header('Display Selected Stduents')
st.write('### The student you selected:', 'student '+ str(student))
st.write('Data Dimension: ' + str(df_selected.shape[0]) + ' rows and ' + str(df_selected.shape[1]) + ' columns.')
st.dataframe(df_selected)

# --- Plot ---
fig = px.bar(df_selected, x = 'session', y = option,
            color = 'activity', barmode = 'stack',
            color_discrete_sequence=px.colors.qualitative.Set3,
            title=("Student" + ' ' + str(student) + ' ' + option))

st.write('### The log activity you selected:', option)
st.plotly_chart(fig, use_container_width=True)