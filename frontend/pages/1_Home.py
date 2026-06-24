"""
CrisisGuardian AI - Home Portal
===============================
Presents project overviews, real-time statistics panels, system architectures,
and tech stack breakdowns.
"""

import streamlit as st
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - Home",
    page_icon="🛡️",
    layout="wide"
)

# Inject styling and sidebar branding
inject_custom_styles()
render_sidebar_branding()

# Header Section
st.markdown("<div class='page-title'>CrisisGuardian AI</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Multi-Agent Emergency Response and Disaster Assistance System</div>", unsafe_allow_html=True)

# 1. Telemetry Statistics Grid
st.markdown("### 📊 SYSTEM METRICS")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown(
        """
        <div class='glass-card'>
            <div class='metric-val' style='color:#a78bfa;'>6</div>
            <div class='metric-label'>Active Agents</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col2:
    st.markdown(
        """
        <div class='glass-card'>
            <div class='metric-val' style='color:#60a5fa;'>4</div>
            <div class='metric-label'>MCP Tools Bound</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col3:
    st.markdown(
        """
        <div class='glass-card'>
            <div class='metric-val' style='color:#34d399;'>100%</div>
            <div class='metric-label'>System Health</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col4:
    st.markdown(
        """
        <div class='glass-card'>
            <div class='metric-val' style='color:#facc15;'>1,482</div>
            <div class='metric-label'>Risk Assessments</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 2. Project Overview & Features
st.markdown("---")
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("### 🛡️ PROJECT OVERVIEW")
    st.write(
        "CrisisGuardian AI is an advanced, multi-agent assistant designed for real-time disaster "
        "response coordination. During critical emergencies like floods, cyclones, earthquakes, or wildfires, "
        "the platform acts as a digital first-responder: aggregating data feeds, evaluating active threat levels, "
        "discovering open shelter facilities, and providing clear, authoritative survival guidelines."
    )
    
    st.markdown("### 🌟 KEY CAPABILITIES")
    st.markdown(
        """
        - **Intelligent Dispatch Supervisor**: Dynamically classifies distress statements and assigns target tasks to specific agent domains.
        - **Modular Hazard Domains**: Four specialized agents containing pre-verified instructions for specific emergency types.
        - **Resource Locator**: Automatically indexes safe houses, emergency hospitals, and municipal relief camps.
        - **Live Alert Tracking**: Connects to global registries (e.g. USGS Seismology feeds) to display warnings.
        """
    )

with col_right:
    st.markdown("### 🧬 ARCHITECTURE OVERVIEW")
    st.write(
        "The system operates as an orchestrator graph built upon LangGraph. Incoming prompts are processed by the "
        "Coordinator Agent, routed to data retrieval agents, checked against structural risk indices, and formatted "
        "into clear survival actions. In-context memory is preserved throughout execution to ensure consistent advice."
    )
    
    # Render mini-mermaid or architecture summary block
    st.markdown(
        """
        <div class='glass-card' style='background:rgba(99,102,241,0.05); border-color:rgba(99,102,241,0.2);'>
            <h5 style='margin:0 0 10px 0; color:#c7d2fe;'>Multi-Agent Pipeline Routing:</h5>
            <code style='font-family:JetBrains Mono, monospace; font-size:0.8rem; color:#818cf8;'>
                START ➔ Coordinator ➔ Weather ➔ News ➔ Resource ➔ Risk ➔ Response ➔ END
            </code>
            <p style='margin:10px 0 0 0; font-size:0.85rem; color:#9ca3af;'>
                Every execution cycles through the 6 agents, calling APIs (MCP Tools) for live data extraction before generating guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. Technology Stack Grid
st.markdown("---")
st.markdown("### 💻 TECHNOLOGY STACK")
tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown(
        """
        <div class='glass-card' style='text-align:center;'>
            <h4 style='color:#a855f7; margin:0;'>Google ADK</h4>
            <p style='font-size:0.85rem; color:#9ca3af; margin:5px 0 0 0;'>Core agent structures and SDK interface</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with tech_col2:
    st.markdown(
        """
        <div class='glass-card' style='text-align:center;'>
            <h4 style='color:#6366f1; margin:0;'>LangGraph</h4>
            <p style='font-size:0.85rem; color:#9ca3af; margin:5px 0 0 0;'>Multi-agent coordination state graphs</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with tech_col3:
    st.markdown(
        """
        <div class='glass-card' style='text-align:center;'>
            <h4 style='color:#2dd4bf; margin:0;'>FastAPI & MCP</h4>
            <p style='font-size:0.85rem; color:#9ca3af; margin:5px 0 0 0;'>REST endpoints & Model Context Protocol</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with tech_col4:
    st.markdown(
        """
        <div class='glass-card' style='text-align:center;'>
            <h4 style='color:#ec4899; margin:0;'>Gemini 2.5 Flash</h4>
            <p style='font-size:0.85rem; color:#9ca3af; margin:5px 0 0 0;'>High-speed LLM reasoning engine</p>
        </div>
        """,
        unsafe_allow_html=True
    )
