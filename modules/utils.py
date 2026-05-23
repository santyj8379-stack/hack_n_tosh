import requests
import re
import streamlit as st

def initialize_http_session(context):
    """Creates an authenticated requests session pre-configured with active parameters."""
    session = requests.Session()
    session.auth = (context["username"], context["password"])
    
    if context["cookie"]:
        session.cookies.set('PHPSESSID', context["cookie"])
        
    return session

def clean_response_text(html_text):
    """Removes standard repetitive layout tags to isolate target strings."""
    # Strip common header/footer components if necessary
    return html_text.strip()