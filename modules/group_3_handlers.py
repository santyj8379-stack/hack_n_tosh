import streamlit as st
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    st.info(f"Analyzing header attributes and session telemetry for {level_name}...")
    
    session = initialize_http_session(context)
    try:
        # Build standard header overrides using dashboard variables
        headers = {"User-Agent": context["user_agent"]}
        response = session.get(context["url"], headers=headers, timeout=10)
        
        st.success("Telemetry request completed.")
        st.write(f"Active Session Context Tracking Identifier: `{context['cookie']}`")
        
        with st.expander("Analyze Traversal State Canvas"):
            st.code(response.text, language="html")
    except Exception as e:
        st.error(f"Error executing module: {str(e)}")