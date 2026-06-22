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
            # =========================================================================
            # RESOURCE AGENT API INTEGRATION POINT:
            # Here, the client queries the FastAPI portal's resource lookup endpoint,
            # which delegates to tools/resource_tool.py via the ResourceAgent.
            #
            # Example API Request:
            #   response = requests.get(f"{BACKEND_URL}/api/resources?location={target_location}")
            #   if response.status_code == 200:
            #       resources = response.json()
            # =========================================================================
            
            # Placeholder data representing database mappings
            shelters = [
                {"name": "District Cyclone Shelter Hall A", "address": "Bay Road, Visakhapatnam", "capacity": "450/600", "distance": "0.8 miles"},
                {"name": "Govt Higher Secondary Safe Center", "address": "Station Road, Visakhapatnam", "capacity": "210/400", "distance": "1.5 miles"}
            ]
            
            hospitals = [
                {"name": "City Emergency Trauma Center", "address": "Main Boulevard, Visakhapatnam", "status": "Critical Load", "distance": "1.2 miles"},
                {"name": "St. Mary Medical Ward", "address": "Park Avenue, Visakhapatnam", "status": "Available Beds", "distance": "2.4 miles"}
            ]
            
            responders = [
                {"station": "Coastal Fire Station Depot 4", "distance": "1.1 miles", "status": "Active Rescue Dispatch"},
                {"police": "Visakhapatnam Central Police Division", "distance": "0.9 miles", "status": "Patrol & Escort Active"}
            ]

        st.success(f"Discovered resources matching area: '{target_location}'")
        
        # Display Columns
        col_shelters, col_hospitals, col_responders = st.columns(3, gap="large")
        
        with col_shelters:
            st.markdown("### 🏠 EMERGENCY SHELTERS")
            for shelter in shelters:
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #6366f1;'>
                        <h5 style='margin:0; color:#c7d2fe;'>{shelter['name']}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>📍 {shelter['address']}</p>
                        <div style='display:flex; justify-content:space-between; margin-top:10px; font-size:0.8rem;'>
                            <span style='color:#34d399;'>Capacity: {shelter['capacity']}</span>
                            <span style='color:#818cf8;'>🚗 {shelter['distance']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        with col_hospitals:
            st.markdown("### 🏥 HOSPITALS & CLINICS")
            for hospital in hospitals:
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #ec4899;'>
                        <h5 style='margin:0; color:#fbcfe8;'>{hospital['name']}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>📍 {hospital['address']}</p>
                        <div style='display:flex; justify-content:space-between; margin-top:10px; font-size:0.8rem;'>
                            <span style='color:#f472b6;'>Status: {hospital['status']}</span>
                            <span style='color:#f472b6;'>🚗 {hospital['distance']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        with col_responders:
            st.markdown("### 🚒 RESCUE & POLICE")
            for unit in responders:
                name = unit.get("station") or unit.get("police")
                st.markdown(
                    f"""
                    <div class='glass-card' style='border-left: 4px solid #2dd4bf;'>
                        <h5 style='margin:0; color:#ccfbf1;'>{name}</h5>
                        <p style='margin:5px 0; font-size:0.85rem; color:#9ca3af;'>🚗 Distance: {unit['distance']}</p>
                        <div style='margin-top:10px; font-size:0.8rem;'>
                            <span style='background:rgba(45,212,191,0.15); color:#2dd4bf; padding:2px 8px; border-radius:10px;'>
                                {unit['status']}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
