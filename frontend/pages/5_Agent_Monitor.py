"""
CrisisGuardian AI - Agent Monitor
===================================
Visualizes the execution pipeline of the multi-agent system.
Displays live agent statuses from the backend API.
"""

import os
import streamlit as st
import requests
import time
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - Agent Monitor",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

AGENT_DEFINITIONS = [
    ("coordinator_agent", "Coordinator Agent", "Orchestrates user queries and coordinates routing."),
    ("weather_agent", "Weather Agent", "Retrieves real-time weather alerts and warnings."),
    ("news_agent", "News Agent", "Queries active emergency news and civil defense announcements."),
    ("resource_agent", "Resource Agent", "Locates shelters, safety stations, and clinics."),
    ("risk_agent", "Risk Agent", "Computes final combined danger index."),
    ("response_agent", "Response Agent", "Compiles actionable guidance checklist lists."),
]

st.markdown("<div class='page-title'>Agent Monitor</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Visualize the operational states and execution telemetry of the active agent network</div>", unsafe_allow_html=True)

# Fetch live agent status from backend
agent_statuses = {}
backend_online = False
try:
    response = requests.get(f"{BACKEND_URL}/agent-status", timeout=3)
    if response.status_code == 200:
        agent_statuses = response.json()
        backend_online = True
except Exception:
    pass

if backend_online:
    st.success("Connected to backend — showing live agent status.")
else:
    st.info("Backend offline — showing default agent states.")

agents_pipeline = []
for key, name, role in AGENT_DEFINITIONS:
    api_status = agent_statuses.get(key, "unknown")
    is_active = api_status == "active"
    agents_pipeline.append({
        "id": key.replace("_agent", ""),
        "name": name,
        "role": role,
        "status": "Success" if is_active else "Idle",
        "exec_time": "—",
        "last_run": "Live" if backend_online else "Unknown",
        "api_status": api_status
    })

# Interactive Simulation Button
st.markdown("### ⚡ RUN SIMULATION RUN")
simulate_pipeline = st.button("▶️ Trigger Simulated Graph Run")

if simulate_pipeline:
    progress_bar = st.progress(0)
    status_text = st.empty()

    for index, ag in enumerate(agents_pipeline):
        status_text.markdown(f"**Executing Node:** `{ag['name']}` ...")
        progress_bar.progress(int((index + 1) / len(agents_pipeline) * 100))
        ag["status"] = "Active"

        st.markdown(
            f"""
            <div class='glass-card' style='border-color:#10b981; background:rgba(16,185,129,0.05);'>
                <h5 style='margin:0; color:#34d399;'>⚡ ACTIVE: {ag['name']}</h5>
                <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>{ag['role']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.6)
        ag["status"] = "Success"

    status_text.success("Graph execution run finished successfully!")
    progress_bar.empty()

# Static / Default Display of Multi-Agent Pipeline Flow
st.markdown("---")
st.markdown("### 🔗 ORCHESTRATION PIPELINE STRUCTURE")

cols = st.columns(len(agents_pipeline))

for idx, ag in enumerate(agents_pipeline):
    with cols[idx]:
        status = ag["status"]
        if status == "Active":
            border_color = "#3b82f6"
            badge = "<span style='color:#60a5fa;'>● Running</span>"
        elif status == "Success":
            border_color = "#10b981"
            badge = f"<span style='color:#34d399;'>● {ag.get('api_status', 'active').title()}</span>"
        else:
            border_color = "rgba(255,255,255,0.08)"
            badge = "<span style='color:#9ca3af;'>● Idle</span>"

        st.markdown(
            f"""
            <div class='glass-card' style='border-color:{border_color}; min-height: 220px; display:flex; flex-direction:column; justify-content:space-between;'>
                <div>
                    <h5 style='margin:0; color:#f3f4f6;'>{ag['name']}</h5>
                    <p style='margin:5px 0; font-size:0.75rem; color:#9ca3af; line-height:1.3;'>{ag['role']}</p>
                </div>
                <div style='margin-top:15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px;'>
                    <div style='font-size:0.8rem; margin-bottom:3px;'>Status: {badge}</div>
                    <div style='font-size:0.75rem; color:#9ca3af;'>Last Check: {ag['last_run']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if idx < len(agents_pipeline) - 1:
            st.markdown(
                """
                <div style='text-align: center; margin-top: 10px; color: #6366f1; font-weight: 800;'>
                    ➔
                </div>
                """,
                unsafe_allow_html=True
            )
