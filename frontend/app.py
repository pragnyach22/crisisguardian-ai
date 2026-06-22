"""
CrisisGuardian AI - Streamlit Dashboard Entrypoint
===================================================
Launches the multi-page dashboard shell and redirects to the Home page.
"""

import streamlit as st

# Set page configurations as first Streamlit command
st.set_page_config(
    page_title="CrisisGuardian AI - Emergency Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Route execution immediately to the Home page module
try:
    st.switch_page("pages/1_Home.py")
except Exception as e:
    st.error(f"Failed to route to home page. Details: {e}")
    st.info("Ensure the pages directory exists and pages/1_Home.py is accessible.")
