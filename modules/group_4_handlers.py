import streamlit as st
import importlib
import os
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    
    session = initialize_http_session(context)
    base_url = context['url'].rstrip('/')
    
    module_filename = level_name.lower().replace(" ", "")
    current_dir = os.path.dirname(__file__)
    
    # Target directory path for standalone Group 4 level modules
    group4_dir_path = os.path.join(current_dir, "group_4")
    sub_module_path = os.path.join(group4_dir_path, f"{module_filename}.py")
    
    # ROUTE TO STANDALONE MODULE IF IT EXISTS
    if os.path.exists(sub_module_path) and os.path.exists(os.path.join(group4_dir_path, "__init__.py")):
        try:
            dynamic_path = f"modules.group_4.{module_filename}"
            target_module = importlib.import_module(dynamic_path)
            target_module.run(context, session, base_url)
            return
        except Exception as err:
            st.error(f"Failed to execute sub-module file: {str(err)}")
            return

    # BACKWARD COMPATIBLE MONOLITHIC FALLBACK
    st.info(f"Analyzing telemetry attributes for {level_name}...")
    try:
        headers = {"User-Agent": context.get("user_agent", "Streamlit-Scanner")}
        response = session.get(base_url, headers=headers, timeout=10)
        
        st.success("Telemetry request completed.")
        with st.expander("Analyze Traversal State Canvas"):
            st.code(response.text, language="html")
    except Exception as e:
        st.error(f"Error executing fallback framework module: {str(e)}")