import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import pickle

from epm.user_db.user_db import create_usertable, add_userdata, get_userdata, view_all_users, delete_usertable
from epm.graph import *
from epm.modeling import review_alert, ml_modeling as mlm

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
        # tentative
        if st.sidebar.checkbox('Delete UserDB'):
            delete_usertable()
        
        # tentative
        st.subheader("User Profiles")
        create_usertable()
        user_result = view_all_users()
        if user_result:
            clean_db = pd.DataFrame(user_result, columns=['Username', 'Password', 'Role'])
            st.dataframe(clean_db)
        else:
            st.warning('No data in userDB') 
        page_home()

    elif choice == 'Log In':
        st.sidebar.subheader('Log In')

        role = st.sidebar.selectbox('Student or Instructor?', ['Student', 'Instructor'])
        username = ""
        if role == 'Instructor':
            username = st.sidebar.text_input('ID', placeholder='admin')
        else:
            student_ids = list(range(1,116))
            username = st.sidebar.selectbox('Student ID', student_ids)
        password = st.sidebar.text_input('Password', type="password", placeholder='password for your ID')

        if st.sidebar.checkbox("Log In"):
            create_usertable()
            result = get_userdata(username, password, role)

            if result and role == 'Instructor':

                st.sidebar.success(f"Welcome to the instructor page, {username}")
                page_instructor()

            elif result and role == 'Student':
                st.sidebar.success(f"Welcome to the student page, {username}")
                page_student(username)

            else:
                st.sidebar.warning("Incorrect Username/Password")
                

    elif choice == 'Sign Up':
        st.subheader("Create New Account")
        new_role = st.selectbox('Student or Instructor?', ['Student', 'Instructor'])
        new_username = ""
        if new_role == 'Instructor':
            new_username = st.text_input('ID', placeholder='admin')
        else:
            student_ids = list(range(1,116))
            new_username = st.selectbox('Student ID', student_ids)
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            create_usertable()
            add_userdata(new_username, new_password, new_role)
            new_userdata = get_userdata(new_username, new_password, new_role)
            if new_userdata:
                st.success("You have successfully created a valid account")
                st.info("Go to Login Menu to login")
            else:
                st.warning("The inserted ID is already taken. Try a different ID")

    else:
        page_about()



def page_home():
    st.header("Home")
    st.image("static/homepage.png")
    st.markdown("""

    # Welcome! Instructors and Students!

    > This website aims to provide visualizations and predictions based on our machine 
    learning model to help you make sense of log data representing your online learning behaviors.
    > 

    If you have any suggestions, please visit our [**GitHub Repo**](https://github.com/EPM-LearningAnalytics/epm) 
    and raise a new issue!

    ## Services Provided:

    1. **💻 Behavioral Analysis:** Showing the distribution of log activities across different types of activities for each session.
        1. Which activity you engaged with the most
        2. Which session you spent most time on
    2. **💯 Grades:** Showing the distribution of grades in one session, and the changes of session grades across 6 sessions. You'll know
        1. For each session, how you performed compared to the whole class
        2. Across 6 sessions, how your grades changed
    3. **📚 For Students - Review Alert:** predictions based on our machine learning models
        1. If you got **Review!**, it indicates that you need to review this session before final in order to 
        answer questions related to this session in the final correctly.
        2. If you got **Safe**, it indicates that you can spend less time on this session since we 
        predict that you already know the content pretty well.
    4. 👩‍🏫 **For** **instructors - Grouping Assistant:** 
        1. Students will be grouped into number of groups based on their performance level, 
        and instructors can make class project groups with similar performance level. 

    ## Navigation Instruction:

    On the sidebar, you can `Sign Up`or `Log In`""")
    st.image("static/menu.png")

    st.markdown("""
    Once you logged in, you can select which sections you'd like to focus on
        
    **For students:**

        """)
    st.image("static/student.png")
    
    st.markdown("""
        **For Instructor:**""")
    st.image("static/instructor.png")
        

    st.markdown("""
    ---------------------------------
    **This website is supported by:**

    Streamlit | Docker | Altair | Sklearn""")

    st.image("static/tech.png")

# --- Student Page ---
def page_student(username):
    st.header("Student page")
    option = st.selectbox("Options to choose", ['Behavior Analysis', 'Grades', 'Review Alert'])
    student = int(username)
    if option == 'Behavior Analysis':
        st.header("Behavior Analysis")
    
        st.markdown("""|Activity|Description|
        |---|---|---|---|
        |**`Aulaweb`**|Learning management system on Moodle|
        |**`Blank`**|When the title of a visited page is not recorded|
        |**`Diagram`**|Testing the timing simulation of the logic network|
        |**`FSM`**|Workinng on a exercise onn 'Finite State Machine Simulator'|
        |**`Deeds`**|Doing activities related to circuit emage or export VHDL|
        |**`Properties`**|Testing the required parameters under construction|
        |**`Study`**|Viewing study materials relevant to the course|
        |**`TextEditor`**|Using the text editor but not doing exercise
        |**`Other`**|When the student is not viewing any pages above|""")

        # read in dataframe
        df = session_agg()
        df_avg = session_avg(df)

        # Selectbox - log activity selection
        log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 
                        'mouse_wheel_click','mouse_click_right',
                        'mouse_movement','keystroke']
        option = st.selectbox(
        '1. Which log activity you like to focus on?',
        log_activity)

        # Multiselect - Activity selection
        sorted_activity_unique = sorted( df['activity'].unique() )
        selected_activity = st.multiselect('2. Which activity do you want to include', 
                                                sorted_activity_unique,
                                                sorted_activity_unique)
        
        # --- Class Average Plot ---
        p = plot_log(df_avg, student, selected_activity, option, type='average').properties(
            title = 'Class Average')

        # --- Student Activity Distribution Plot ---
        s = plot_log(df, student, selected_activity, option, type='student').properties(
            title='Student' + ' ' + str(student) + ' ' + option)

        # Present graphs side by side
        x = alt.hconcat(
            p, s
        ).resolve_scale(y='shared')
        st.write('**Plot Result**: You select ' + option)
        st.write(x)

    elif option == 'Grades':
        st.header("Grades")
        # --- each session histogram plot ---
        session = st.radio('Which session?', (2, 3, 4, 5, 6), 0)
        
        # prepare datasets
        data_for_hist = mid_hist(session)
        data_summary = mid_summary(student, data_for_hist)

        p = plot_mid_hist(session, student, data_for_hist, data_summary)

        st.write(p)
        # --- session grades plot ---
        # prepare datasets
        all, area = mid_avg()

        all = all[all['Student Id'].isin(['Average',str(student)])]

        m = plot_mid(all, area)

        st.write(m)
    else:
        page_review_alert(username)

# --- Instructor Page ---
def page_instructor():
    st.header("This is the instructor page")
    option = st.selectbox("Options to choose", ['Class Behavior Analysis', 'Class Grades', 
                                                'Grouping Assistant'])
    
    if option == 'Class Behavior Analysis':
        
        st.markdown("""|Activity|Description|
        |---|---|---|---|
        |**`Aulaweb`**|Learning management system on Moodle|
        |**`Blank`**|When the title of a visited page is not recorded|
        |**`Diagram`**|Testing the timing simulation of the logic network|
        |**`FSM`**|Workinng on a exercise onn 'Finite State Machine Simulator'|
        |**`Deeds`**|Doing activities related to circuit emage or export VHDL|
        |**`Properties`**|Testing the required parameters under construction|
        |**`Study`**|Viewing study materials relevant to the course|
        |**`TextEditor`**|Using the text editor but not doing exercise
        |**`Other`**|When the student is not viewing any pages above|""")
            
        # read in dataframe
        df = session_agg()
        df_avg = session_avg(df)

        # Slider - Student Slider 
        student = st.slider('1. Which student?', 1, 115)

        # Selectbox - log activity selection
        log_activity = ['mouse_click_left','mouse_wheel', 'idle_time', 
                        'mouse_wheel_click','mouse_click_right',
                        'mouse_movement','keystroke']
        option = st.selectbox(
        '2. Which log activity you like to focus on?',
        log_activity)

        # Multiselect - Activity selection
        sorted_activity_unique = sorted( df['activity'].unique() )
        selected_activity = st.multiselect('3. Which activity do you want to include', 
                                                sorted_activity_unique,
                                                sorted_activity_unique)

        # --- Class Average Plot ---
        p = plot_log(df_avg, student, selected_activity, option, type='average').properties(
            title = 'Class Average')

        # --- Student Activity Distribution Plot ---
        s = plot_log(df, student, selected_activity, option, type='student').properties(
            title='Student' + ' ' + str(student) + ' ' + option)

        # Present graphs side by side
        x = alt.hconcat(
            p, s
        ).resolve_scale(y='shared')

        st.write('**Plot Result**: You select ' + 'student ' + str(student) + ' and ' + option)
        st.write(x)

    elif option == 'Class Grades':
        st.header("Class Grades")
        # --- each session histogram plot ---
        col1, col2 = st.columns(2)
        with col1:
            session = st.radio('Which session?', (2, 3, 4, 5, 6), 0)
        with col2:
            student = st.number_input('Which student you want to focus on \
                                      (input student ID from 1 to 115)', 1, 115, 1)
        
        # prepare datasets
        data_for_hist = mid_hist(session)
        data_summary = mid_summary(student, data_for_hist)

        p = plot_mid_hist(session, student, data_for_hist, data_summary)

        st.write(p)
        # --- session grades plot ---
        # prepare datasets
        all, area = mid_avg()

        students = all['Student Id'].unique()
        selected_students = st.multiselect('Students you selected', 
                                                students,
                                                ['Average', '1'])
        all = all[all['Student Id'].isin(selected_students)]

        m = plot_mid(all, area)

        st.write(m)

    elif option == 'Grouping Assistant':
        page_grouping_assistant()


def page_about():
    st.title("About Us")
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:  
        st.image("static/member_photos/teemo.png",width=200)
        st.markdown(
            """
            ## Meredith  
            <b><font color="#005CB9" face="Helvetica" size="3.5">Visualization Team</font> </b>   
            <br/><br/>
            **\"Go Huskies!\"**  
            <br/>
            :email:<b><font color="#FF5733" face="Verdana" size="2.5">mereluo@uw.edu</font> </b>
            """
            ,unsafe_allow_html= True
            )
        
    with col2:       
        st.image("static/member_photos/teemo.png",width=200)
        st.markdown(
            """
            ## Seyoung
            <b><font color="#005CB9" face="Helvetica" size="3.5">Web Development Team</font> </b>    
            <br/><br/>
            **\"I love EPM!\"**  
            <br/>
            :email:<b><font color="#FF5733" face="Verdana" size="2.5">synam@uw.edu</font> </b>
            """
            ,unsafe_allow_html= True
            )

    with col3:
        st.image("static/member_photos/teemo.png",width=200)
        st.markdown(
            """
            ## Yongwon
            <b><font color="#005CB9" face="Helvetica" size="3.5">Machine Learning Team</font> </b>
            <br/><br/>  
            **\"I love EPM!\"**  
            <br/>
            :email:<b><font color="#FF5733" face="Verdana" size="2.5">kimyw@uw.edu</font> </b>
            """,
            unsafe_allow_html = True
            )

    with col4: 
        st.image("static/member_photos/teemo.png",width=200)
        st.markdown(
            """
            ## Wenjin
            <b><font color="#005CB9" face="Helvetica" size="3.5">Visualization Team</font> </b>
            <br/><br/>  
            **\"Yinsheng is my boss!\"**  
            <br/>
            :email:<b><font color="#FF5733" face="Verdana" size="2.5">wjzhang@uw.edu</font> </b>
            """
            ,unsafe_allow_html= True
            )

    with col5:    
        st.image("static/member_photos/ys.PNG",width=200)
        st.markdown(
            """
            ## Yinsheng
            <b><font color="#005CB9" face="Helvetica" size="3.5">Machine Learning Team</font> </b>
            <br/><br/>  
            **\"If I die, I die.\"**  
            <br/>
            :email:<b><font color="#FF5733" face="Verdana" size="2.5">kysheng@uw.edu</font> </b>
            """
            ,unsafe_allow_html= True
            ) 

def page_behavior_analysis(id):
    st.header("Behavior Analysis")

def page_grades(id):
    st.header("Grades")

def page_review_alert(username):
    st.header("Review Alert")
    res = review_alert(username)[2:]

    for i, col in enumerate(st.columns(5)):
        label = "Session " + str(i+2)
        value = "Review!" if res[i] == 1 else "Safe"
        col.metric(label, value)

def page_grouping_assistant():
    st.header("Grouping Assistant")

    #Read data
    objects = []
    with (open("epm/data_prep/pickles/whole_data.pkl", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    whole_data = objects[0]



    whatever= '<p style="font-family:Arial; color:Blue; font-size: 20px;">User input features</p>'

    st.sidebar.header("User input features")
    features_include =  st.sidebar.selectbox("How many siginificant learning features to be included?",range(2,5))
    cluster_timing =  st.sidebar.selectbox("Which session is the class at?",range(2,7))
    number_of_cluster = int(st.sidebar.text_input("How many clusters to make?", 3))

    with st.spinner('Compiling model...'):
        gif_runner = st.image('static/loading.gif')
        subdata = mlm.subset_important_features(whole_data,features_include,"common")
        cluster_result = mlm.kmean_clustering(subdata,cluster_timing,number_of_cluster)

        input_dropdown = alt.binding_select(options=np.array(range(number_of_cluster)))
        selection = alt.selection_single(fields=['group'], 
                                        bind=input_dropdown,
                                        name='Cluster of')
        color = alt.condition(selection,
                            alt.Color('group:N', legend=None),
                            alt.value('lightgray'))
        x = f"{cluster_result.columns.values[0]}:Q"
        y = f"{cluster_result.columns.values[-2]}:Q"
        c = alt.Chart(cluster_result).mark_point().encode(
                x=x,
                y=y,
                color=color,
                tooltip='ID:Q'
            ).add_selection(
                selection
            ).properties(
                width=800,
                height=600
            )
        gif_runner.empty()

        st.altair_chart(c, use_container_width=False)
        st.write(cluster_result[['ID','group']].transpose())

    

if __name__ == "__main__":
    main()
