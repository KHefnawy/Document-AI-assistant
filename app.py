import streamlit as st
import os
from global_settings import initialize_settings
from conversation_engine import initialize_chatbot, chat_interface, load_chat_store


def show_chat_UI():
    st.header(f"Document Q&A System")
    
    # Chatbot integration
    st.success(f"Hello. I'm here to answer questions about your documents.")
    chat_store = load_chat_store()
    container = st.container(height=600)
    agent = initialize_chatbot(chat_store, container)
    chat_interface(agent, chat_store, container)

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title('Document Q&A System')
    st.sidebar.markdown('### Your Personal Document Assistant')

    # Initialize settings
    initialize_settings()
    show_chat_UI()

if __name__ == "__main__":
    main()
