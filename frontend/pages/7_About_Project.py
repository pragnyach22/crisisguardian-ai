"""
CrisisGuardian AI - About Project
=================================
Presents background details, design parameters, developer guides,
and workflow diagrams.
"""

import streamlit as st
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - About",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

st.markdown("<div class='page-title'>About the Project</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Development background, multi-agent orchestrations, and future outlook</div>", unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("### 🔍 PROBLEM STATEMENT")
    st.write(
        "During natural disasters (cyclones, floods, earthquakes, wildfires), critical seconds determine "
        "survival. Citizens face severe challenges: fragmented municipal bulletins, social media disinformation, "
        "congested safety lines, and difficulty finding safe zones or medical capacities nearby. "
        "First responder networks need automated assistant agents that can verify alerts, locate relief camps, "
        "and present clean, direct survival protocols to the public."
    )
    
    st.markdown("### 💡 THE SOLUTION")
    st.write(
        "CrisisGuardian AI addresses these concerns by deploying a coordinated net of specialized safety agents. "
        "Built using LangGraph and powered by Gemini 2.5 Flash, the supervisor coordinates weather forecasting, news crawling, "
        "and shelter querying tasks in a deterministic state flow. By standardizing safety instructions, it delivers "
        "reliable, context-verified advice in critical moments."
    )

with col_right:
    st.markdown("### 🧬 MULTI-AGENT STATE FLOW")
    st.write(
        "The application utilizes LangGraph to ensure strict sequential validation, preventing logical hallucination in critical situations:"
    )
    
    # Textual diagram representation
    st.markdown(
        """
        <div class='glass-card'>
            <pre style='font-family:JetBrains Mono, monospace; font-size:0.8rem; color:#a78bfa; margin:0;'>
[User distress signal]
      ↓
(1) Coordinator Agent (Extracts target area)
      ↓
(2) Weather Agent (Fetches warnings via MCP)
      ↓
(3) News Agent (Verifies municipal notices)
      ↓
(4) Resource Agent (Locates hospitals & shelters)
      ↓
(5) Risk Agent (Calculates threat tier index)
      ↓
(6) Response Agent (Generates step-by-step guidance)
      ↓
[Actionable Responder Report]
            </pre>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
col_bottom_left, col_bottom_right = st.columns(2, gap="large")

with col_bottom_left:
    st.markdown("### 🛠️ CORE SPECIFICATIONS")
    st.markdown(
        """
        - **LLM Reasoning**: Google Gemini 2.5 Flash (via `langchain-google-genai`).
        - **Agent Framework**: Google Agent Development Kit (ADK) + LangChain.
        - **Workflow State Machine**: LangGraph StateGraph.
        - **Geospatial & Search Tools**: Model Context Protocol (MCP) integrations.
        - **Service Layer**: FastAPI REST API portal (Uvicorn).
        - **User Presentation Layer**: Streamlit Multi-page Dashboard.
        """
    )
    
    st.markdown("### 👨‍💻 DEVELOPER INFO")
    st.write(
        "**CrisisGuardian AI Capstone Project**\n"
        "- **Framework**: Code-first Python (ADK + LangGraph)\n"
        "- **Repository**: crisisguardian-ai\n"
        "- **Development Stage**: Initial multi-agent integration templates successfully validated."
    )

with col_bottom_right:
    st.markdown("### 🚀 FUTURE ENHANCEMENTS")
    st.markdown(
        """
        1. **Geospatial GeoJSON Mapping**: Integrate real-time interactive mapping layers (e.g., Folium/Leaflet) directly in the Resource Finder to show active flood zones.
        2. **SMS Gateway / SOS Dispatch**: Wire the Resource Agent's simulated SOS dispatch tool to Twilio or similar platforms to dispatch actual SMS safety updates to citizens.
        3. **RAG Vector Database integration**: Connect the Document Analyzer to persistent vector databases (e.g., ChromaDB / FAISS) for long-term document vector lookups.
        4. **Broadcasting alerts**: Build push-based WebSocket servers to broadcast storm bulletins to active users.
        """
    )
