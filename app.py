import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt

from userDB.userDB import create_usertable, add_userdata, login_user, view_all_users
# from epm.graph_data import *


def main():
    components.html(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">
        <div class="row">
            <div class="alignleft" style="text-align: justify;">
                <svg width="70" height="40" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect y="165" width="180" height="15" rx="5" fill="#D1D5DB"/>
                    <rect y="3" width="37" height="156" rx="5" fill="#7ACBCD"/>
                    <rect x="45" y="3" width="37" height="156" rx="5" fill="#FB8282"/>
                    <rect x="88" y="13.2224" width="37" height="156" rx="5" transform="rotate(-20.9382 88 13.2224)" fill="#7B61FF"/>
                </svg>            
            </div>
            <div class="alignleft" style="text-align: justify;">
                <h1>Educational Process Mining</h1>            
            </div>
        </div>
        """
    )

    menu = ['Home', 'Log In', 'Sign Up', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        page_home()

    elif choice == 'Log In':
        st.sidebar.subheader('Log In')

        role = st.sidebar.selectbox('Student or Instructor?', ['Student', 'Instructor'])
        username = st.sidebar.text_input('ID', placeholder='35')
        password = st.sidebar.text_input('Password', type="password", placeholder='password for ID 35')

        if st.sidebar.checkbox("Log In"):
            create_usertable()
            result = login_user(username, password)

            if result and role == 'Instructor':
                st.sidebar.success(f"Welcome to the instructor page, {username}")
                page_instructor()

            elif result and role == 'Student':
                st.sidebar.success(f"Welcome to the student page, {username}")
                page_student(id)

            else:
                st.sidebar.warning("Incorrect Username/Password")
                

    elif choice == 'Sign Up':
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created a valid account")
            st.info("Go to Login Menu to login")

    else:
        page_about()



def page_home():
    st.header("Home")


def page_student(id):
    st.header("Student page")
    option = st.selectbox("Options to choose", ['Behavior Analysis', 'Grades', 'Review Alert'])
    
    if option == 'Behavior Analysis':
        st.header("Behavior Analysis")
    elif option == 'Grades':
        st.header("Grades")
    else:
        st.header("Review Alert")


def page_instructor():
    st.header("This is the instructor page")
    option = st.selectbox("Options to choose", ['Class Behavior Analysis', 'Class Grades', 'Grouping Assistant', 'User Profiles'])
    
    if option == 'Class Behavior Analysis':
        st.header("Class Behavior Analysis")
        print(os.getcwd())
        # --- read in dataframe ---
        df_avg = pd.read_csv('./EPM_dataset/Data/class_avg_mere.csv')
        df = pd.read_csv('./EPM_dataset/Data/log_session_mere.csv')

        # --- Slider - Student Slider ---
        student = st.slider('Which student?', 1, 115)


        # --- Selectbox - log activity selection ---
        log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 'mouse_wheel_click',
                        'mouse_click_right','mouse_movement','keystroke']
        option = st.selectbox(
            'Which log activity you like to focus on?',
            log_activity
        )

        # --- Multiselect - Activity selection ---
        sorted_activity_unique = sorted( df['activity'].unique() )

        selected_activity = st.multiselect('Activity', 
                                                sorted_activity_unique,
                                                sorted_activity_unique)


        # --- Filtering data ---
        df_selected = df[ (df['activity'].isin(selected_activity)) & (df['student_id'] == student) ]
        df_avg_selected = df_avg[ (df['activity'].isin(selected_activity)) ]


        # --- Display dataframe ---
        # st.header('Display Selected Stduents')
        st.write('### The student you selected:', 'student '+ str(student))
        # st.write('Data Dimension: ' + str(df_selected.shape[0]) + ' rows and ' + str(df_selected.shape[1]) + ' columns.')
        # st.dataframe(df_selected.drop(df_selected.columns[[0, 1, 2]], axis=1))


        # --- Class Average Plot ---

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

    elif option == 'Class Grades':
        st.header("Class Grades")

    elif option == 'Grouping Assistant':
        st.header("Grouping Assistant")

    else:
        st.subheader("User Profiles")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result, columns=['Username', 'Password'])
        st.dataframe(clean_db)        



def page_about():
    st.header("About page")

def page_behavior_analysis(id):
    st.header("Behavior Analysis")

def page_grades(id):
    st.header("Grades")

def page_review_alert(id):
    st.header("Review Alert")

if __name__ == "__main__":
    main()
