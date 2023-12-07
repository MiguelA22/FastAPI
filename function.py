from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import faiss
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import PyPDFLoader

import streamlit as st

def get_vectorstore(text_chunk):
    embeddings = OpenAIEmbeddings()
    vectorstore = faiss.FAISS.from_documents(documents=text_chunk,embedding=embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

def get_conversation_chain(vectostore):
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    llm = ChatOpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectostore,
        memory = memory
    )
    return conversation_chain

def get_chunks_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap  = 500,
        length_function = len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_extension(data):
    extension = data.name.split('.')[-1]
    return extension

def get_pdf_text(data):
    text = ""
    pdf_text = PdfReader(data)
    for page in pdf_text.pages:
        text += page.extract_text()
    return text

def pdf_loader(pdf):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf.getvalue())
        tmp_file_path = tmp_file.name
    loader = PyPDFLoader(tmp_file_path)
    data = loader.load()
    return data

def csv_loader(csv):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(csv.getvalue())
        tmp_file_path = tmp_file.name
    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8",csv_args={'delimiter': ','})
    data = loader.load()
    return data
    

def userinput(question):
    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(message.content)
        else:
            st.write(message.content)

def process_files(data):
    for file in data:
        extension = get_extension(file)

        if extension == "pdf":
            #raw_text = get_pdf_text(file)
            #text_chunk = get_chunks_text(raw_text)
            data = pdf_loader(file)
            vectostore = get_vectorstore(data)
            st.session_state.conversation = get_conversation_chain(vectostore)
            
        elif extension == "csv":
            data = csv_loader(file)
            vectostore = get_vectorstore(data)
            st.session_state.conversation = get_conversation_chain(vectostore)
            #return tmp_file_path
        else:
            return "This type of file is not accepted"

    
        