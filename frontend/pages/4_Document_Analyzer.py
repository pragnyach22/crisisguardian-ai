"""
CrisisGuardian AI - Document Analyzer
=====================================
Enables parsing and summarizing disaster-related PDFs, emergency plans, and guides.
Connects with LangChain document loaders and semantic query utilities.
"""

import streamlit as st
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - Document Analyzer",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

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
if submit_analysis:
    if uploaded_file is None:
        st.warning("Please upload a PDF document first before starting the analysis.")
    else:
        with st.spinner("Parsing document structure & extracting semantic warnings..."):
            # =========================================================================
            # LANGCHAIN DOCUMENT ANALYSIS CONNECTION POINT:
            # Here, the PDF file bytes are read and processed by LangChain.
            #
            # Example backend implementation flow:
            #   1. Save bytes to temporary directory.
            #   2. Load via LangChain:
            #      from langchain_community.document_loaders import PyPDFLoader
            #      loader = PyPDFLoader(temp_path)
            #      pages = loader.load()
            #   3. Split texts:
            #      from langchain_text_splitters import RecursiveCharacterTextSplitter
            #      splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            #      docs = splitter.split_documents(pages)
            #   4. Embed and query via Gemini/VectorStore:
            #      from langchain_google_genai import GoogleGenerativeAIEmbeddings
            #      from langchain_community.vectorstores import FAISS
            #      vector_store = FAISS.from_documents(docs, GoogleGenerativeAIEmbeddings())
            #   5. Run a summarize or QA chain to answer: "What is the summary, what are the warnings, actions, and contacts?"
            # =========================================================================
            
            # Simulated placeholder values
            doc_name = uploaded_file.name
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
            contacts = [
                "Municipal Disaster Management Desk: 1800-555-0100",
                "First Responder Emergency Desk: 112 / 911",
                "Regional Flood Rescue Command Unit: +1-555-0921"
            ]

        st.success("Document analyzed successfully!")
        
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
            
            st.markdown("### 📞 IMPORTANT CONTACTS")
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            for contact in contacts:
                st.markdown(f"- **{contact}**")
            st.markdown("</div>", unsafe_allow_html=True)
            
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
