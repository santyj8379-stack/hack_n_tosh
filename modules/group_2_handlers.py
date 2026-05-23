import streamlit as st
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    st.info(f"Targeting input and parameter manipulation validation configurations for {level_name}...")
    
    session = initialize_http_session(context)
    try:
        response = session.get(context["url"], timeout=10)
        st.success("Connection parameters verified.")
        with st.expander("Inspect Raw Response Body"):
            st.code(response.text, language="html")
    except Exception as e:
        st.error(f"Error executing module: {str(e)}")