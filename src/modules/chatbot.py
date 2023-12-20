import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
import langchain

langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    qa_template = """
        You are a helpful academic assistant named CET Advisement Bot, or CAB. The user gives you a file and its content is represented by the following pieces of context. Use them to answer the question at the end.
        You are also aware of important academic advisement information. This includes information such as the maximum amount of credits a student can take per semester, which is 18.
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.

        context: {context}
        =========
        question: {question}
        ======
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

    def conversational_chat(self, query):
        """
        Chat using LLM through LangChain framework
        """
        #model
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        #use vectorstore for information retrieval
        retriever = self.vectors.as_retriever()

        #chain using parameters defined directly above
        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, return_source_documents=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        #append new messages to history & show response
        st.session_state["history"].append((query, result["answer"]))
        return result["answer"]

    
    
