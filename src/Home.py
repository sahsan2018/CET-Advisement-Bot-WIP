import streamlit as st


#Config
st.set_page_config(layout="wide", page_title="CET Advisement Bot (Preliminary Stage)")

#Title
st.markdown(
    """
    <h2 style='text-align: center;'>CET Advisement Bot, Work In Progress</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>I am the precursor to a fully developed academic advisement bot for City Tech. 
    Currently, I can read and answer questions about PDF files.</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("Pages")
st.write("""
- **Chat**: Functional chat on user provided PDF files.
""")
st.markdown("---")
