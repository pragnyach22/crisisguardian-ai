"""
CrisisGuardian AI - Resource Finder
===================================
Enables location-based lookup of shelters, hospitals, police, and fire dispatch.
Integrates with resource_agent capabilities.
"""

import streamlit as st
import requests
import os
from utils import inject_custom_styles, render_sidebar_branding

# Page Setup
st.set_page_config(
    page_title="CrisisGuardian AI - Resource Finder",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_sidebar_branding()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.markdown("<div class='page-title'>Resource Finder</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Locate medical centers, emergency shelter domes, and local responders</div>", unsafe_allow_html=True)

# 1. Location Input Panel
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 📍 Geographical Search")
    
    target_location = st.text_input(
        "Enter City, Postal Code, or Coordinates:",
        placeholder="e.g. Visakhapatnam, Andhra Pradesh or 17.6868° N, 83.2185° E",
        value="Visakhapatnam, AP"
    )
    
    submit_search = st.button("🗺️ Find Resources", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Resource Results
if submit_search:
    if not target_location.strip():
        st.warning("Please enter a valid location to run the locator.")
    else:
        with st.spinner(f"Resolving critical assets near {target_location}..."):
            is_mock = False
            backend_error = None
            shelters = []
            hospitals = []
            police_stations = []
            fire_stations = []

            try:
                response = requests.post(
                    f"{BACKEND_URL}/resources",
                    json={"location": target_location},
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    shelters = data.get("shelters", [])
                    hospitals = data.get("hospitals", [])
                    police_stations = data.get("police_stations", [])
                    fire_stations = data.get("fire_stations", [])
                else:
                    backend_error = f"Backend returned status {response.status_code}"
                    raise Exception(backend_error)
            except Exception as e:
                backend_error = backend_error or str(e)
                is_mock = True
                shelters = [
                    {"name": "District Cyclone Shelter Hall A", "address": "Bay Road", "capacity": "450/600", "distance_miles": 0.8, "status": "Open"},
                    {"name": "Govt Higher Secondary Safe Center", "address": "Station Road", "capacity": "210/400", "distance_miles": 1.5, "status": "Open"}
                ]
                hospitals = [
                    {"name": "City Emergency Trauma Center", "address": "Main Boulevard", "status": "Critical Load", "distance_miles": 1.2},
                    {"name": "St. Mary Medical Ward", "address": "Park Avenue", "status": "Available Beds", "distance_miles": 2.4}
                ]
                police_stations = [{"name": "Central Police Division", "distance_miles": 0.9, "status": "Patrol Active"}]
                fire_stations = [{"name": "Coastal Fire Station Depot 4", "distance_miles": 1.1, "status": "Active Rescue Dispatch"}]

        st.success(f"Discovered resources matching area: '{target_location}'")
        if is_mock:
            st.info("Backend unavailable — showing local fallback data.")
            if backend_error:
                st.warning(f"Backend request error: {backend_error}")
        
        # Display Columns
        col_shelters, col_hospitals, col_responders = st.columns(3, gap="large")
        
        with col_shelters:
            st.markdown("### 🏠 EMERGENCY SHELTERS")
            for shelter in shelters:
                dist = shelter.get("distance_miles", shelter.get("distance", "N/A"))
                dist_label = f"{dist} mi" if isinstance(dist, (int, float)) else str(dist)
                capacity = shelter.get("capacity", shelter.get("status", "Unknown"))
                address = shelter.get("address", "Address unavailable")
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #6366f1;'>
                        <h5 style='margin:0; color:#c7d2fe;'>{shelter['name']}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>📍 {address}</p>
                        <div style='display:flex; justify-content:space-between; margin-top:10px; font-size:0.8rem;'>
                            <span style='color:#34d399;'>Capacity: {capacity}</span>
                            <span style='color:#818cf8;'>🚗 {dist_label}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        with col_hospitals:
            st.markdown("### 🏥 HOSPITALS & CLINICS")
            for hospital in hospitals:
                dist = hospital.get("distance_miles", hospital.get("distance", "N/A"))
                dist_label = f"{dist} mi" if isinstance(dist, (int, float)) else str(dist)
                status = hospital.get("status", "Unknown")
                address = hospital.get("address", "Address unavailable")
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #ec4899;'>
                        <h5 style='margin:0; color:#fbcfe8;'>{hospital['name']}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>📍 {address}</p>
                        <div style='display:flex; justify-content:space-between; margin-top:10px; font-size:0.8rem;'>
                            <span style='color:#f472b6;'>Status: {status}</span>
                            <span style='color:#f472b6;'>🚗 {dist_label}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        with col_responders:
            st.markdown("### 🚒 RESCUE & POLICE")
            responders = []
            for ps in police_stations:
                responders.append({"name": ps.get("name", ps.get("station", "Police Station")), "distance_miles": ps.get("distance_miles", ps.get("distance", "N/A")), "status": ps.get("status", "Active")})
            for fs in fire_stations:
                responders.append({"name": fs.get("name", fs.get("station", "Fire Station")), "distance_miles": fs.get("distance_miles", fs.get("distance", "N/A")), "status": fs.get("status", "Ready")})
            for unit in responders:
                dist = unit.get("distance_miles", "N/A")
                dist_label = f"{dist} mi" if isinstance(dist, (int, float)) else str(dist)
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #2dd4bf;'>
                        <h5 style='margin:0; color:#ccfbf1;'>{unit['name']}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>🚗 Distance: {dist_label}</p>
                        <div style='margin-top:10px; font-size:0.8rem;'>
                            <span style='background:rgba(45,212,191,0.15); color:#2dd4bf; padding:2px 8px; border-radius:10px;'>
                                {unit['status']}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
