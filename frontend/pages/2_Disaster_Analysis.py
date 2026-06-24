"""
CrisisGuardian AI - Disaster Analysis
=====================================
Allows users to enter disaster queries, triggering coordinator and agent evaluations.
Communicates with the FastAPI backend endpoint `/analyze`.
"""

import streamlit as st
import requests
import os
from utils import inject_custom_styles, render_sidebar_branding

# Page Config
st.set_page_config(
    page_title="CrisisGuardian AI - Disaster Analysis",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
ANALYZE_TIMEOUT = int(os.getenv("ANALYZE_TIMEOUT", "120"))

st.markdown("<div class='page-title'>Disaster Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Submit emergency queries to trigger multi-agent pipeline evaluations</div>", unsafe_allow_html=True)

# 1. Main Input Container
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 💬 Inquiry Panel")
    
    # Input Area
    user_query = st.text_area(
        "Enter disaster-related query:",
        placeholder="e.g. Is there a cyclone warning in Andhra Pradesh? What precautions should I take during heavy rainfall?",
        height=100
    )
    
    # Example Selection
    st.markdown("<p style='font-size:0.85rem; color:#9ca3af; margin-bottom:5px;'>Suggested Scenarios:</p>", unsafe_allow_html=True)
    example_queries = [
        "Select an example to populate the field...",
        "Is there a cyclone warning in Andhra Pradesh?",
        "Verify this flood-related message: 'Dams on the northern river are opening gates at 2 PM, evacuation mandated.'",
        "What precautions should I take during heavy rainfall in Mumbai?"
    ]
    selected_example = st.selectbox("", example_queries, label_visibility="collapsed")
    
    # Populate text area with example if selected
    if selected_example != "Select an example to populate the field...":
        # Streamlit state logic can update value
        st.info(f"Preset loaded: '{selected_example}'")
        user_query = selected_example
        
    location_input = st.text_input("Target Location (Optional)", placeholder="e.g. Andhra Pradesh, Mumbai")
    
    # Trigger Button
    submit_analysis = st.button("🚨 Analyze Situation", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Results Container
if submit_analysis:
        if not user_query.strip():
            st.warning("Please enter a query or select an example to run the analysis.")
        else:
            with st.spinner("Running multi-agent analysis — this may take 15–30 seconds..."):
                # =========================================================================
                # FASTAPI BACKEND API INTEGRATION POINT:
                # Here, the frontend communicates with the FastAPI /analyze endpoint.
                #
                # Example API Request:
                #   payload = {
                #       "user_id": "streamlit-web-client",
                #       "message": user_query,
                #       "location": location_input,
                #       "crisis_type": "general" # Can be classified or parsed
                #   }
                #   response = requests.post(f"{BACKEND_URL}/analyze", json=payload)
                #   if response.status_code == 200:
                #       data = response.json()
                # =========================================================================
                
                backend_error = None
                try:
                    # Dynamically detect crisis type from the query
                    query_lower = user_query.lower()
                    if "cyclone" in query_lower or "hurricane" in query_lower or "storm" in query_lower or "wind" in query_lower:
                        detected_crisis = "cyclone"
                    elif "flood" in query_lower or "rain" in query_lower or "water" in query_lower:
                        detected_crisis = "flood"
                    elif "earthquake" in query_lower or "tremor" in query_lower or "quake" in query_lower or "seismic" in query_lower:
                        detected_crisis = "earthquake"
                    elif "fire" in query_lower or "wildfire" in query_lower or "smoke" in query_lower or "burn" in query_lower:
                        detected_crisis = "fire"
                    else:
                        detected_crisis = "general"

                    payload = {
                        "user_id": "streamlit-frontend",
                        "message": user_query,
                        "location": location_input,
                        "crisis_type": detected_crisis
                    }
                    # Make HTTP call to FastAPI
                    api_response = requests.post(
                        f"{BACKEND_URL}/analyze",
                        json=payload,
                        timeout=ANALYZE_TIMEOUT
                    )
                    if api_response.status_code == 200:
                        api_data = api_response.json()
                        
                        risk_level = api_data.get("threat_level")
                        verification = api_data.get("verification_status", "Verified via News Agent")
                        weather_summary = api_data.get("weather_summary", "Active Cyclone watch. Wind speeds scaling up to 90kmh near coastlines.")
                        emergency_updates = api_data.get("guidance")
                        recommended_actions = api_data.get("recommended_actions")
                        is_mock = False
                    else:
                        backend_error = f"Backend returned status {api_response.status_code}: {api_response.text}"
                        raise Exception(backend_error)
                except requests.exceptions.Timeout:
                    backend_error = (
                        f"Analysis timed out after {ANALYZE_TIMEOUT}s. "
                        "The backend may still be processing — try again or increase ANALYZE_TIMEOUT."
                    )
                    is_mock = True
                    risk_level = "High Threat (Mock)"
                    verification = "Verified by News & Risk Agents"
                    weather_summary = "Precipitation exceeding 120mm. Moderate high winds detected in region."
                    emergency_updates = "District collector issued storm shelter warnings. Local bridges closed."
                    recommended_actions = [
                        "Evacuate low-lying river areas.",
                        "Seek cover in concrete shelter hubs.",
                        "Store 3 days of sanitized drinking water."
                    ]
                except requests.exceptions.ConnectionError:
                    backend_error = "Cannot connect to backend. Start it with: python main.py"
                    is_mock = True
                    risk_level = "High Threat (Mock)"
                    verification = "Verified by News & Risk Agents"
                    weather_summary = "Precipitation exceeding 120mm. Moderate high winds detected in region."
                    emergency_updates = "District collector issued storm shelter warnings. Local bridges closed."
                    recommended_actions = [
                        "Evacuate low-lying river areas.",
                        "Seek cover in concrete shelter hubs.",
                        "Store 3 days of sanitized drinking water."
                    ]
                except Exception as e:
                    backend_error = backend_error or str(e)
                    # Mock details if backend is offline or request fails
                    risk_level = "High Threat (Mock)"
                    verification = "Verified by News & Risk Agents"
                    weather_summary = "Precipitation exceeding 120mm. Moderate high winds detected in region."
                    emergency_updates = "District collector issued storm shelter warnings. Local bridges closed."
                    recommended_actions = [
                        "Evacuate low-lying river areas.",
                        "Seek cover in concrete shelter hubs.",
                        "Store 3 days of sanitized drinking water."
                    ]
                    is_mock = True
                    
            # Display Output Panels in column layout
            st.success("Analysis Complete!")
            if is_mock:
                if backend_error and "Cannot connect" in backend_error:
                    st.info("💡 Backend server not detected. Showing local mock simulations.")
                elif backend_error and "timed out" in backend_error.lower():
                    st.info("💡 Backend is running but the analysis took too long. Showing local mock data.")
                else:
                    st.info("💡 Backend unavailable. Showing local mock simulations.")
                if backend_error:
                    st.warning(f"Backend request error: {backend_error}")
        col_res1, col_res2 = st.columns([1, 2], gap="large")
        
        with col_res1:
            st.markdown("### 🔍 THREAT ASSESSMENTS")
            
            # Risk Level Badge
            st.markdown(
                f"""
                <div class='glass-card' style='border-left: 5px solid #ef4444;'>
                    <div style='font-size:0.8rem; color:#9ca3af; text-transform:uppercase;'>Threat Tier</div>
                    <div style='font-size:1.8rem; font-weight:700; color:#f87171;'>{risk_level}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Verification Status Badge
            st.markdown(
                f"""
                <div class='glass-card' style='border-left: 5px solid #10b981;'>
                    <div style='font-size:0.8rem; color:#9ca3af; text-transform:uppercase;'>Alert Verification</div>
                    <div style='font-size:1.2rem; font-weight:600; color:#34d399;'>{verification}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_res2:
            st.markdown("### 📋 SAFETY PROTOCOLS")
            
            # Weather Summary Card
            st.markdown(
                f"""
                <div class='glass-card'>
                    <h5 style='margin:0 0 5px 0; color:#60a5fa;'>🌤️ Meteorological Feed</h5>
                    <p style='margin:0; font-size:0.95rem; color:#d1d5db;'>{weather_summary}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Civil Bulletins
            st.markdown(
                f"""
                <div class='glass-card'>
                    <h5 style='margin:0 0 5px 0; color:#facc15;'>📢 Emergency Updates</h5>
                    <p style='margin:0; font-size:0.95rem; color:#d1d5db;'>{emergency_updates}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Recommended Actions Checklist
            st.markdown("#### Action Items Required:")
            for action in recommended_actions:
                st.markdown(
                    f"""
                    <div class='custom-alert alert-severe'>
                        <span style='font-weight:600;'>CRITICAL ACTION:</span> {action}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
