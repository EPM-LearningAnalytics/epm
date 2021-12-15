import codecs
import streamlit as st
import streamlit.components.v1 as components
import base64


file = codecs.open("justtry/aboutus.html", "r", "utf-8")
about_us = file.read()
file.close()


# embed streamlit docs in a streamlit app
components.iframe("justtry/aboutus.html")


# components.html(
#     about_us,
#     height=4000,
#     width=1200,
#     scrolling= True
# )
