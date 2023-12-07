import streamlit as st
from st_pages import Page, show_pages, add_page_title

from function import userinput

from dotenv import load_dotenv

load_dotenv()

with st.container():
    #prompt = st.chat_input("Make your question...")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    prompt = st.text_input("Ask your questions", label_visibility="collapsed")
    with st.chat_message("user"):
        st.write(prompt)

    if prompt:
        with st.spinner():
            with st.chat_message("ai"):
                userinput(prompt)