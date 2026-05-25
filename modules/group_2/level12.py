import streamlit as st

def run(context, session, base_url):
    st.info("Level 12 Sub-Module Active: Examining file validation context...")
    
    try:
        # Establish base connection to pull the current form token or upload interface
        response = session.get(base_url, timeout=10)
        st.success("Successfully reached Level 12 endpoint target.")
        
        # Display metadata context inside metrics layout columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="HTTP Status", value=response.status_code)
        with col2:
            st.write("**Active Headers Context:**", dict(response.headers))
            
        # Render response inspection tray
        with st.expander("Inspect Raw Response Body"):
            st.code(response.text, language="html")
            
    except Exception as e:
        st.error(f"Level 12 connection routine failed: {str(e)}")