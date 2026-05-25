import streamlit as st
import re
import base64

def run(context, session, base_url):
    st.info("Level 11 sub-module active: Processing token generation and state handling...")
    
    try:
        initial_response = session.get(base_url, timeout=10)
        default_json = '{"showpassword":"no","bgcolor":"#ffffff"}'
        default_cookie = session.cookies.get("data")
        
        if default_cookie:
            st.write(f"Captured Default Cookie: `{default_cookie}`")
            cipher_bytes = base64.b64decode(default_cookie.replace("%3D", "="))
            plain_bytes = default_json.encode('utf-8')
            key_pattern = bytes([p ^ c for p, c in zip(plain_bytes, cipher_bytes)])
            
            # Key recovery extraction logic
            fragment = key_pattern[:4]  # 'eDWo' string fragment
            key_string = fragment.decode('utf-8', errors='ignore')
            st.success(f"🔑 Derived Encryption Key Signature: `{key_string}`")
            
            # Generate the winning payload state
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
                st.code(f"Next Level Password: {valid_tokens[0]}")
            else:
                st.warning("Request completed but no matching password signature was found in the text.")
            
            with st.expander("Inspect Raw Response Body"):
                st.code(authenticated_response.text, language="html")
        else:
            st.warning("No tracking cookie discovered in headers.")
            
    except Exception as e:
        st.error(f"Sub-module execution failed: {str(e)}")