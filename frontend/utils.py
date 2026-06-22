"""
CrisisGuardian AI - Frontend Styling and Utilities
===================================================
Provides shared styling functions, CSS injectors, and layout headers.
"""

import streamlit as st

def inject_custom_styles():
    """
    Injects custom CSS to achieve a premium dark-themed, glassmorphic appearance
    with custom typography and responsive layout grids.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');
        
        /* General layout overrides */
        .stApp {
            background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
            font-family: 'Outfit', sans-serif;
            color: #f3f4f6;
        }
        
        /* Sidebar styling override */
        section[data-testid="stSidebar"] {
            background-color: rgba(17, 24, 39, 0.9) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(8px);
        }
        
        /* Custom card */
        .glass-card {
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.4);
        }
        
        /* Custom headers */
        .page-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .page-subtitle {
            font-size: 1rem;
            color: #9ca3af;
            margin-bottom: 1.8rem;
        }
        
        /* System status indicator */
        .status-dot {
            height: 10px;
            width: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-online { background-color: #10b981; box-shadow: 0 0 8px #10b981; }
        .status-offline { background-color: #ef4444; box-shadow: 0 0 8px #ef4444; }
        .status-warning { background-color: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
        
        /* Metric container styling */
        .metric-val {
            font-size: 2.2rem;
            font-weight: 700;
            color: #f3f4f6;
            margin-bottom: 0.1rem;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Alert boxes */
        .custom-alert {
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .alert-severe { background: rgba(239, 68, 68, 0.12); border-left: 5px solid #ef4444; }
        .alert-warning { background: rgba(245, 158, 11, 0.12); border-left: 5px solid #f59e0b; }
        .alert-safe { background: rgba(16, 185, 129, 0.12); border-left: 5px solid #10b981; }
        
        /* Button overrides */
        .stButton>button {
            background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_sidebar_branding():
    """
    Renders custom branding text and badges in the sidebar.
    """
    st.sidebar.markdown(
        """
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.08);'>
            <h2 style='margin: 0; background: linear-gradient(90deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>🛡️ CrisisGuardian</h2>
            <p style='margin: 2px 0 0 0; font-size: 0.8rem; color: #9ca3af;'>MULTI-AGENT OPERATIONS</p>
            <div style='margin-top: 10px; display: inline-flex; align-items: center; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 9999px; padding: 2px 10px;'>
                <span class="status-dot status-online"></span>
                <span style='font-size: 0.7rem; color: #34d399; font-weight: 600;'>SYSTEM ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
