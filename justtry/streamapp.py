from re import S
import streamlit as st
import pandas as pd
import numpy as np
import pickle

import altair as alt
from sklearn.ensemble import RandomForestClassifier
from yw import ml_modeling as mlm

st.write("""
# Clustering students 

**This app cluster students by their overall performance!**

""")

#Read data
objects = []
with (open("justtry/yw/whole_data.pkl", "rb")) as openfile:
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
number_of_cluster = st.sidebar.text_input("How many clusters to make?", 3)
st.sidebar.markdown(whatever,unsafe_allow_html=True)

number_of_cluster =int(number_of_cluster)

with st.spinner('Compiling model...'):
    gif_runner = st.image('justtry/loading.gif')
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
    