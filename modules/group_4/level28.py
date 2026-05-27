import streamlit as st
import base64

def run(context, session, base_url):
    st.info("Targeting Cryptographic ECB Block Alignment & Telemetry Mapping...")
    
    # 1. Align active level credentials using your new Level 28 token
    username = "natas28"
    current_password = context.get('password', '').strip()
    session.auth = (username, current_password)
    
    target_url = "http://natas28.natas.labs.overthewire.org/index.php"
    
    try:
        # 2. Fire structural probe variations to observe ciphertext size fluctuations
        st.write("📡 Running differential input size analysis...")
        
        for input_len in [1, 2, 3, 4, 10, 16, 20]:
            test_query = "A" * input_len
            
            # Post the query to trigger the search routine redirect mechanism
            # We catch the redirect manually or read the final URL to get the 'query' cipher text
            response = session.post(target_url, data={"query": test_query}, allow_redirects=False)
            
            # Extract the raw location header containing the query hash string
            redirect_location = response.headers.get("Location", "")
            
            if "query=" in redirect_location:
                raw_cipher = redirect_location.split("query=")[1]
                # Decode from URL encoding if necessary, and check raw byte length
                decoded_bytes = base64.b64decode(requests.utils.unquote(raw_cipher)) if 'requests' in locals() else b""
                st.write(f" ├─ Input: {input_len} chars -> Ciphertext Length: `{len(raw_cipher)}` base64 characters")
            else:
                st.write(f" ├─ Input: {input_len} chars -> No redirect token found.")
                
        st.success("Telemetry mapping complete. Review ciphertext sizes to calculate structural blocks.")
        
    except Exception as e:
        st.error(f"Execution failed due to programmatic error: {str(e)}")