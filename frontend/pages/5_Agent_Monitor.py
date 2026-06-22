"""
CrisisGuardian AI - Agent Monitor
=================================
Visualizes the execution pipeline of the multi-agent system.
Displays live statuses, mock execution times, and pipeline traces.
"""

import streamlit as st
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

st.markdown("<div class='page-title'>Agent Monitor</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Visualize the operational states and execution telemetry of the active agent network</div>", unsafe_allow_html=True)

# Define agent pipeline data
agents_pipeline = [
    {
        "id": "coordinator",
        "name": "Coordinator Agent",
        "role": "Orchestrates user queries and coordinates routing.",
        "status": "Idle",
        "exec_time": "120 ms",
        "last_run": "2 mins ago"
    },
    {
        "id": "weather",
        "name": "Weather Agent",
        "role": "Retrieves real-time weather alerts and warnings.",
        "status": "Idle",
        "exec_time": "450 ms",
        "last_run": "2 mins ago"
    },
    {
        "id": "news",
        "name": "News Agent",
        "role": "Queries active emergency news and civil defense announcements.",
        "status": "Idle",
        "exec_time": "380 ms",
        "last_run": "2 mins ago"
    },
    {
        "id": "resource",
        "name": "Resource Agent",
        "role": "Locates shelters, safety stations, and clinics.",
        "status": "Idle",
        "exec_time": "290 ms",
        "last_run": "2 mins ago"
    },
    {
        "id": "risk",
        "name": "Risk Agent",
        "role": "Computes final combined danger index.",
        "status": "Idle",
        "exec_time": "150 ms",
        "last_run": "2 mins ago"
    },
    {
        "id": "response",
        "name": "Response Agent",
        "role": "Compiles actionable guidance checklist lists.",
        "status": "Idle",
        "exec_time": "620 ms",
        "last_run": "2 mins ago"
    }
]

# Interactive Simulation Button
st.markdown("### ⚡ RUN SIMULATION RUN")
simulate_pipeline = st.button("▶️ Trigger Simulated Graph Run")

# =========================================================================
# FUTURE SYSTEM MONITORING & TELEMETRY INTEGRATION:
# In future deployment, we will connect this page to real-time execution logs
# of the LangGraph state machine. Every node execution fires an event that
# updates the Streamlit interface using WebSockets or status API checks.
#
# Example connection workflow:
#   1. Read transaction run session ID.
#   2. Request execution state trace from FastAPI backend:
#      trace = requests.get(f"{BACKEND_URL}/api/runs/{run_id}/trace")
#   3. Parse graph steps (nodes activated, completed, inputs/outputs).
# =========================================================================

# If simulated run is clicked
if simulate_pipeline:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for index, ag in enumerate(agents_pipeline):
        status_text.markdown(f"**Executing Node:** `{ag['name']}` ...")
        # Update progress
        progress_bar.progress(int((index + 1) / len(agents_pipeline) * 100))
        # Update agent status in dict
        ag["status"] = "Active"
        
        # Render visual card dynamically with green border while active
        st.markdown(
            f"""
            <div class='glass-card' style='border-color:#10b981; background:rgba(16,185,129,0.05);'>
                <h5 style='margin:0; color:#34d399;'>⚡ ACTIVE: {ag['name']}</h5>
                <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>{ag['role']}</p>
                <div style='font-size:0.8rem; color:#d1d5db; margin-top:5px;'>
                    <span>Execution: {ag['exec_time']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.6)
        ag["status"] = "Success"
        st.rerun = True
        
    status_text.success("Graph execution run finished successfully!")
    progress_bar.empty()

# Static / Default Display of Multi-Agent Pipeline Flow
st.markdown("---")
st.markdown("### 🔗 ORCHESTRATION PIPELINE STRUCTURE")

# Horizontal flow using column panels
cols = st.columns(len(agents_pipeline))

for idx, ag in enumerate(agents_pipeline):
    with cols[idx]:
        # Status styling
        status = ag["status"]
        if status == "Active":
            border_color = "#3b82f6"
            badge = "<span style='color:#60a5fa;'>● Running</span>"
        elif status == "Success":
            border_color = "#10b981"
            badge = "<span style='color:#34d399;'>● Completed</span>"
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
                    <div style='font-size:0.75rem; color:#9ca3af;'>Latency: {ag['exec_time']}</div>
                    <div style='font-size:0.75rem; color:#9ca3af;'>Last Run: {ag['last_run']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Draw connector arrow (except for the last agent)
        if idx < len(agents_pipeline) - 1:
            st.markdown(
                """
                <div style='text-align: center; margin-top: 10px; color: #6366f1; font-weight: 800;'>
                    ➔
                </div>
                """,
                unsafe_allow_html=True
            )
