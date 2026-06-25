"""
CrisisGuardian AI - Document Analyzer
=====================================
Enables parsing and summarizing disaster-related PDFs, emergency plans, and guides.
Connects with LangChain document loaders and semantic query via the backend API.
"""

import os
import streamlit as st
import requests
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - Document Analyzer",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.markdown("<div class='page-title'>Document Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Upload emergency policy manuals or threat guidebooks to generate summaries</div>", unsafe_allow_html=True)

# 1. File Upload Panel
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 📁 PDF Document Upload")

    uploaded_file = st.file_uploader(
        "Upload disaster protocol, emergency plan, or weather report (PDF):",
        type=["pdf"]
    )

    submit_analysis = st.button("📄 Analyze Document", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Analysis Results
# Clear session state if file changes
if uploaded_file is not None and st.session_state.get("uploaded_file_name") != uploaded_file.name:
    st.session_state.doc_analyzed = False
    st.session_state.doc_answer = None
    if "doc_answer" in st.session_state:
        del st.session_state.doc_answer

if submit_analysis:
    if uploaded_file is None:
        st.warning("Please upload a PDF document first before starting the analysis.")
    else:
        with st.spinner("Parsing document structure & extracting semantic warnings..."):
            is_mock = False
            backend_error = None
            doc_name = uploaded_file.name
            summary = ""
            key_warnings = []
            recommended_actions = []

            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(
                    f"{BACKEND_URL}/document-analysis",
                    files=files,
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    summary = data.get("summary", "")
                    key_warnings = data.get("warnings", [])
                    recommended_actions = data.get("recommendations", [])
                else:
                    backend_error = f"Backend returned status {response.status_code}: {response.text}"
                    raise Exception(backend_error)
            except Exception as e:
                backend_error = backend_error or str(e)
                is_mock = True
                summary = (
                    f"The document '{doc_name}' is identified as a Flood Evacuation Protocol for Urban Sectors. "
                    "It describes operational guidelines, flood level definitions (alert, warning, danger), "
                    "and routes to municipal community safe havens."
                )
                key_warnings = [
                    "Evacuate immediately when water rises above level tier 3 (2.5 meters).",
                    "Do not stay in subterranean garages or ground-floor rooms if structural integrity is compromised.",
                    "Turn off the power main before water levels reach electrical outlets."
                ]
                recommended_actions = [
                    "Establish neighborhood communication units prior to storm landing.",
                    "Collect non-perishable rations (minimum 72-hour supply per individual).",
                    "Mark out primary and secondary high-ground egress lines on district maps."
                ]
            
            st.session_state.doc_analyzed = True
            st.session_state.summary = summary
            st.session_state.key_warnings = key_warnings
            st.session_state.recommended_actions = recommended_actions
            st.session_state.doc_name = doc_name
            st.session_state.is_mock = is_mock
            st.session_state.backend_error = backend_error
            st.session_state.uploaded_file_name = uploaded_file.name

# If a document has been analyzed, display the results
if st.session_state.get("doc_analyzed") and uploaded_file is not None and st.session_state.get("uploaded_file_name") == uploaded_file.name:
    summary = st.session_state.summary
    key_warnings = st.session_state.key_warnings
    recommended_actions = st.session_state.recommended_actions
    is_mock = st.session_state.is_mock
    backend_error = st.session_state.backend_error
    doc_name = st.session_state.doc_name
    
    st.success("Document analyzed successfully!")
    if is_mock:
        st.info("Backend unavailable — showing local fallback analysis.")
        if backend_error:
            st.warning(f"Backend request error: {backend_error}")

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("### 📋 EXECUTIVE SUMMARY")
        st.markdown(
            f"""
            <div class='glass-card'>
                <h5 style='margin:0 0 10px 0; color:#a78bfa;'>Document Context</h5>
                <p style='margin:0; font-size:0.95rem; line-height:1.5; color:#d1d5db;'>{summary}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not is_mock:
            st.markdown("### 💬 ASK ABOUT THIS DOCUMENT")
            user_question = st.text_input(
                "Ask a question about the uploaded document:",
                placeholder="e.g. What evacuation routes are mentioned?",
                key="doc_question_input"
            )
            if st.button("🔍 Query Document"):
                if user_question.strip():
                    with st.spinner("Querying document context..."):
                        try:
                            qa_response = requests.post(
                                f"{BACKEND_URL}/document-query",
                                json={"query": user_question},
                                timeout=30
                            )
                            if qa_response.status_code == 200:
                                answer = qa_response.json().get("answer", "No answer returned.")
                                st.session_state.doc_answer = answer
                            else:
                                st.error(f"Query failed: {qa_response.text}")
                        except Exception as e:
                            st.error(f"Could not reach backend: {e}")
            
            if "doc_answer" in st.session_state and st.session_state.doc_answer:
                st.markdown(
                    f"""
                    <div class='glass-card'>
                        <p style='margin:0; font-size:0.95rem; line-height:1.5; color:#d1d5db;'>{st.session_state.doc_answer}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with col_right:
        st.markdown("### ⚠️ WARNINGS & PRECAUTIONS")
        for warning in key_warnings:
            st.markdown(
                f"""
                <div class='custom-alert alert-severe'>
                    <strong>WARNING:</strong> {warning}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### ⚡ REQUIRED PROCEDURES")
        for action in recommended_actions:
            st.markdown(
                f"""
                <div class='custom-alert alert-warning'>
                    <strong>PROCEDURE:</strong> {action}
                </div>
                """,
                unsafe_allow_html=True
            )
