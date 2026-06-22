"""
CrisisGuardian AI FastAPI Application
Defines REST API endpoints for communicating with disaster response agents and workflows.
"""

import os
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from workflows.crisis_workflow import create_crisis_workflow

# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="CrisisGuardian AI Backend",
    description="Multi-Agent Disaster Response Assistant API",
    version="1.0.0"
)

# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# LangGraph Workflow Initialization
# ==========================================================

try:
    workflow_app = create_crisis_workflow()
    print("[INFO] Crisis Workflow initialized successfully.")
except Exception as e:
    print(f"[WARNING] Failed to initialize workflow: {e}")
    workflow_app = None

# ==========================================================
# Request Models
# ==========================================================

class UserQuery(BaseModel):
    user_id: str
    message: str
    location: Optional[str] = None
    disaster_type: Optional[str] = None

# ==========================================================
# Response Models
# ==========================================================

class AgentResponse(BaseModel):
    agent_name: str
    status: str
    response_text: str
    recommended_actions: list[str]
    metadata: Dict[str, Any]

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
async def root():
    return {
        "message": "Welcome to CrisisGuardian AI",
        "status": "online"
    }

# ==========================================================
# Health Check Endpoint
# ==========================================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "CrisisGuardian AI"
    }

# ==========================================================
# Chat Endpoint
# ==========================================================

@app.post("/api/chat", response_model=AgentResponse)
async def chat_disaster_assistant(query: UserQuery):
    """
    Main endpoint for disaster-related queries.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        # --------------------------------------------------
        # Real Workflow Execution
        # --------------------------------------------------
        if workflow_app and api_key and api_key != "your_gemini_api_key_here":
            initial_state = {
                "messages": [
                    HumanMessage(content=query.message)
                ],
                "location": query.location or "unknown location",
                "crisis_type": query.disaster_type or "general",
                "weather_data": None,
                "news_data": None,
                "resource_data": None,
                "risk_level": None,
                "final_guidance": None
            }

            result = workflow_app.invoke(initial_state)

            guidance = result.get(
                "final_guidance",
                "No guidance generated."
            )

            risk = result.get(
                "risk_level",
                "Unknown"
            )

            return AgentResponse(
                agent_name="CrisisWorkflow",
                status="completed",
                response_text=guidance,
                recommended_actions=[
                    f"Risk Level: {risk}"
                ],
                metadata={
                    "location": query.location,
                    "disaster_type": query.disaster_type,
                    "workflow": "crisis_workflow",
                    "model_used": "Gemini 2.5 Flash"
                }
            )

        # --------------------------------------------------
        # Mock Response (No Gemini Key)
        # --------------------------------------------------
        disaster = query.disaster_type or "general"

        return AgentResponse(
            agent_name=f"{disaster.capitalize()}ResponseAgent",
            status="completed_mock",
            response_text=(
                f"Received request regarding {disaster} "
                f"in {query.location or 'unspecified location'}."
            ),
            recommended_actions=[
                "Ensure your immediate physical safety first.",
                "Listen to local emergency broadcasts.",
                "Prepare an emergency go-bag if evacuation is advised."
            ],
            metadata={
                "location": query.location,
                "disaster_type": disaster,
                "model_used": "Mock Fallback"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==========================================================
# Emergency Alerts Endpoint
# ==========================================================

@app.get("/api/alerts")
async def active_alerts(location: Optional[str] = None):
    return {
        "location": location or "Global",
        "alerts": [
            {
                "id": "alert-001",
                "severity": "High",
                "type": "Flood Warning",
                "message": "Heavy rainfall expected to cause flash floods in low-lying areas.",
                "timestamp": "2026-06-22T10:00:00Z"
            }
        ]
    }
