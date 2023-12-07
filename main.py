import streamlit as st

from st_pages import Page, show_pages, add_page_title


from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from dotenv import load_dotenv
import function as ft

def main():
    st.set_page_config(page_title="Holder AI",page_icon=":robot_face:",layout='wide')

    show_pages([
        Page("main.py","Home",":house:"),
        Page("chat.py","Chat",":computer:")
    ])
    load_dotenv()


    #Header
    with st.container():
        st.header("Holder AI :chart_with_upwards_trend:")

    with st.container():
        files_upload = st.file_uploader("Upload your documets",accept_multiple_files=True,type=['csv','pdf'])
        
        if st.button("Upload Data"):
            with st.spinner():
                process = ft.process_files(files_upload)
                st.write(process)


if __name__ =='__main__':
    main()



    
