import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import base64
from google import genai
from google.genai import types
from supabase import create_client
from modules import group_1_handlers, group_2_handlers, group_3_handlers

# ==========================================
# PLATFORM CORE CONFIGURATIONS
# ==========================================
st.set_page_config(page_title="hack_n_tosh Dashboard", layout="wide")

st.title("🤖 hack_n_tosh: Multi-Model Autonomous Engine")
st.subheader("Stable Network Execution Layer & Multi-AI Failover Router")
st.markdown("---")

# ==========================================
# SIDEBAR: Permanent Parameter State
# ==========================================
st.sidebar.header("🎯 Target Parameters")
target_base_url = st.sidebar.text_input("Target Base URL", value="http://natas26.natas.labs.overthewire.org")
username = st.sidebar.text_input("Username", value="natas26")
password = st.sidebar.text_input("Password", value="ckELKUWZUfPOv6uxS6M7lXBpBssJZ4Ws", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🧠 AI Brain Configuration")

ai_provider = st.sidebar.selectbox("Select AI Model Provider", ["Gemini (Google AI)", "Groq (Llama / Mixtral)"])

# DATA STORAGE AND API ROUTING CONFIGURATION
DEFAULT_GEMINI_KEY = "AIzaSyAnciRLYdPDOR345XQFRI..."  # Replace with your actual key
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_ANON_KEY = "your-supabase-anon-key"

# Optional manual tracking adjustments
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Request Interceptor Overrides")
manual_cookie = st.sidebar.text_input("Manual Session Cookie (PHPSESSID)", value="")
custom_user_agent = st.sidebar.text_input("Custom User-Agent Header", value="Mozilla/5.0 (hack_n_tosh/1.0)")

# Initialize External Storage Components Natively
try:
    ai_client = genai.Client(api_key=DEFAULT_GEMINI_KEY)
    supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
except Exception as init_err:
    st.sidebar.error("Client Init Warning: Verify Key Configuration.")

# ==========================================
# MAIN WORKSPACE: Methodology Grouping Engine
# ==========================================
st.header("🛠️ Multi-Level Test Matrix Controller")

methodology_group = st.selectbox(
    "Select Methodology Group:",
    [
        "Group 1: Static Controls & Information Disclosure (Levels 0 - 10)",
        "Group 2: Input Validation & Parameter Control (Levels 11 - 16)",
        "Group 3: Session Tracking & Header Monitoring (Levels 17 - 25)"
    ]
)

# Render individual modules based on group choice
if "Group 1" in methodology_group:
    selected_level = st.selectbox("Select Target Module:", [f"Level {i}" for i in range(11)])
elif "Group 2" in methodology_group:
    selected_level = st.selectbox("Select Target Module:", [f"Level {i}" for i in range(11, 17)])
else:
    selected_level = st.selectbox("Select Target Module:", [f"Level {i}" for i in range(17, 26)])

st.markdown(f"Active Status: **{selected_level}** module framework is armed.")

# ==========================================
# EXECUTION ROUTER TRIPPERS
# ==========================================
if st.button("🚀 Fire Active Verification Module"):
    if not target_base_url or not password:
        st.error("❌ Target URL and Boundary Password are required to run module sequences.")
    else:
        # Building the common context map to pass variables down to modules safely
        context = {
            "url": target_base_url,
            "username": username,
            "password": password,
            "cookie": manual_cookie if manual_cookie else None,
            "user_agent": custom_user_agent,
            "ai_provider": ai_provider,
            "ai_client": ai_client if 'ai_client' in locals() else None,
            "supabase": supabase_client if 'supabase_client' in locals() else None
        }
        
        st.info(f"🔄 Routing engine controls to module handlers for {selected_level}...")
        
        # Call the corresponding module routing function
        if "Group 1" in methodology_group:
            group_1_handlers.execute(selected_level, context)
        elif "Group 2" in methodology_group:
            group_2_handlers.execute(selected_level, context)
        elif "Group 3" in methodology_group:
            group_3_handlers.execute(selected_level, context)

# ==========================================
# PROVISION FOR EXTERNAL HELP APPROACH
# ==========================================
if st.checkbox("🛠️ Show Provision Mode (Manual Assistance & Custom Parameters)"):
    st.markdown("---")
    st.header("🛠️ Provision Mode: Manual Assistance & Custom Parameters")
    st.warning("Automation router halted or custom parameters required. Send arbitrary requests below:")
    
    col1, col2 = st.columns(2)
    with col1:
        custom_endpoint = st.text_input("Custom Target Sub-URL Path", value="index.php")
        param_key = st.text_input("POST Payload Form Key", value="username")
        param_val = st.text_area("Custom Injected Payload Value", value="")
    
    with col2:
        st.markdown("#### ⚙️ Manual Operations Dashboard")
        st.write("Use this workspace to test variations manually when data patterns fluctuate.")
        
        if st.button("⚡ Transmit Custom Request"):
            try:
                session = requests.Session()
                session.auth = (username, password)
                if manual_cookie:
                    session.cookies.set('PHPSESSID', manual_cookie)
                
                custom_data = {param_key: param_val}
                manual_res = session.post(f"{target_base_url}/{custom_endpoint}", data=custom_data)
                st.markdown("**Server Response Box:**")
                st.code(manual_res.text)
            except Exception as manual_error:
                st.error(f"Manual transmit failure: {str(manual_error)}")