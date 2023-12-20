import os
import streamlit as st
import pdfplumber

from modules.chatbot import Chatbot
from modules.embedder import Embedder

class Utilities:

    @staticmethod
    def load_api_key():
        """
        Load API key from .env file or user input
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #.env with API key
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env")
        else:
            #use already exisiting key
            if st.session_state.api_key is not None:
                user_api_key = st.session_state.api_key
                st.sidebar.success("API key loaded from previous input")
            #key from user input
            else:
                user_api_key = st.sidebar.text_input(
                    label="#### Your OpenAI API key", placeholder="sk-...", type="password"
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key

        return user_api_key

    
    @staticmethod
    def handle_upload(file_types):
        """
        method to work with uploaded file, can be expanded to different types beyond PDF
        """
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        # if file uploaded
        if uploaded_file is not None:
            # handle PDFs
            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
            
            # extract file extension (for future updates with multiple file types)
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)

            # Show the contents of the file based on its extension
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
        else:
            st.session_state["reset_chat"] = True

        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # embeddings for upload
            vectors = embeds.getDocEmbeds(file, uploaded_file.name)

            # initialize chatbot based on given parameters
            chatbot = Chatbot(model, temperature,vectors)
        st.session_state["ready"] = True

        return chatbot


    
