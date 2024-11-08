#Purpose: Manages chat interactions
#Components:
#   - load_chat_store(): Loads or creates new chat history
#   - display_messages(): Shows chat history in UI
#   - initialize_chatbot(): Sets up AI agent with memory and tools
#   - chat_interface(): Handles real-time chat interaction

import os
import streamlit as st
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from global_settings import INDEX_STORAGE, CONVERSATION_FILE, STORAGE_PATH
from document_uploader import ingest_documents
from index_builder import build_indexes
from logging_functions import log_action

def load_chat_store():
    try:
        os.makedirs(os.path.dirname(CONVERSATION_FILE), exist_ok=True)
        chat_store = SimpleChatStore.from_persist_path(CONVERSATION_FILE)
    except:
        chat_store = SimpleChatStore()
    return chat_store

def display_messages(chat_store, container):
    print("Displaying messages")
    with container:
        messages = chat_store.get_messages(key="0")
        for message in messages:
            with st.chat_message(message.role):
                st.markdown(message.content)

def initialize_chatbot(chat_store, container):
    memory = ChatMemoryBuffer.from_defaults(token_limit=4096, chat_store=chat_store, chat_store_key="0")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
    vector_index = load_index_from_storage(storage_context, index_id="vector")
    
    query_engine = vector_index.as_query_engine(
        similarity_top_k=10
    )
    
    documents_tool = QueryEngineTool(
        query_engine=query_engine, 
        metadata=ToolMetadata(
            name="documents",
            description="Provides information from the uploaded documents. Use a detailed plain text question as input to the tool.",
        )
    )
    
    agent = OpenAIAgent.from_tools(
        tools=[documents_tool], 
        memory=memory,
        system_prompt=f"You are a helpful assistant. Your purpose is to help answer questions about the uploaded documents. Always provide accurate information"
    )
    
    display_messages(chat_store, container)
    return agent

def chat_interface(agent, chat_store, container):  
    col1, col2 = st.columns([4, 1])
    with col1:
        prompt = st.chat_input("Type your question here:")
    with col2:
        upload_more = st.button("📄 Upload More Docs", key="upload_more")

    if upload_more:
        st.session_state['show_uploader'] = True
        st.session_state['agent'] = None   
        
    if st.session_state.get('show_uploader'):
        uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, key="file_uploader")
        if uploaded_files and st.button("Process Files", key="process_files"):
            with st.spinner("Processing new documents..."):
                try:
                    if save_and_process_files(uploaded_files):
                        st.success("Documents processed successfully!")
                        st.session_state['show_uploader'] = False
                        st.rerun()
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")

    if prompt:
        with container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            response_obj = agent.chat(prompt)
            response = str(response_obj)
            
     
            with st.chat_message("assistant"):
                st.markdown(response)
                
    chat_store.persist(CONVERSATION_FILE)

def save_and_process_files(uploaded_files):        
    for uploaded_file in uploaded_files:
        file_path = os.path.join(STORAGE_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        log_action(f"File '{file_path}' uploaded by user", "UPLOAD")
    
    nodes = ingest_documents()
    build_indexes(nodes)
    
    st.session_state['agent'] = None
    st.session_state['show_uploader'] = False
    
    return True