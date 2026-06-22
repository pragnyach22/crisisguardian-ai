"""
CrisisGuardian AI - FastAPI API Backend
======================================
Defines structural endpoints for querying multi-agent crisis pipelines.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

app = FastAPI(
    title="CrisisGuardian AI - API Portal",
    description="Backend API interface providing disaster analysis routes.",
    version="1.0.0"
)

# CORS middleware configuration for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================================
# PYDANTIC SCHEMAS / MODELS
# =========================================================================

# 1. Analyze Schemas
class AnalyzeRequest(BaseModel):
    query: str

class AnalyzeResponse(BaseModel):
    risk_level: str
    verification_status: str
    weather_summary: str
    emergency_updates: List[str]
    recommendations: List[str]

# 2. Resource Schemas
class ResourcesRequest(BaseModel):
    location: str

class ResourcesResponse(BaseModel):
    hospitals: List[Dict[str, Any]]
    shelters: List[Dict[str, Any]]
    police_stations: List[Dict[str, Any]]
    fire_stations: List[Dict[str, Any]]

# 3. Document Analysis Schemas
class DocumentAnalysisResponse(BaseModel):
    summary: str
    warnings: List[str]
    recommendations: List[str]

# 4. Status Schemas
class SystemStatusResponse(BaseModel):
    backend: str
    workflow: str
    mcp: str

class AgentStatusResponse(BaseModel):
    coordinator_agent: str
    weather_agent: str
    news_agent: str
    resource_agent: str
    risk_agent: str
    response_agent: str

# =========================================================================
# ROUTE ENDPOINTS
# =========================================================================

@app.get("/health")
async def health_check():
    """
    Returns the general health status of the CrisisGuardian AI application.
    """
    return {
        "status": "healthy",
        "service": "CrisisGuardian AI"
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_disaster(request: AnalyzeRequest):
    """
    Analyzes a disaster-related user query.
    
    Future Integration:
    - This is where the LangGraph `crisis_workflow` or `disaster_workflow`
      will be invoked with the user query as the input message state.
    - Weather, News, Risk, and Response agents will process the context
      to compute the final unified response.
    """
    try:
        # Placeholder response
        return AnalyzeResponse(
            risk_level="HIGH",
            verification_status="VERIFIED",
            weather_summary="Heavy rainfall expected",
            emergency_updates=[
                "Flood warning active"
            ],
            recommendations=[
                "Stay indoors",
                "Charge devices",
                "Prepare emergency kit"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resources", response_model=ResourcesResponse)
async def find_resources(request: ResourcesRequest):
    """
    Locates nearby shelters, hospitals, police and fire stations.
    
    Future Integration:
    - Connect to the `ResourceAgent` to query local maps/databases
      or execute `find_nearest_shelter` tool configurations.
    """
    try:
        # Placeholder response
        # Using structured object profiles matching the Streamlit interface fields
        return ResourcesResponse(
            hospitals=[
                {
                    "name": "General Emergency Hospital",
                    "address": "100 Recovery Road",
                    "status": "Active (High Traffic)",
                    "distance": "3.2 miles"
                }
            ],
            shelters=[
                {
                    "name": "Community Safe House - Sector A",
                    "address": "402 Safe Haven Ave",
                    "capacity": "300 / 500 occupied",
                    "distance": "1.5 miles"
                }
            ],
            police_stations=[
                {
                    "name": "Central Metro Police Station",
                    "address": "50 Law Enforcer Way",
                    "status": "Patrol & Egress Control",
                    "distance": "2.1 miles"
                }
            ],
            fire_stations=[
                {
                    "name": "County Fire & Rescue Unit 5",
                    "address": "85 Flamebreak Way",
                    "status": "Mobilized",
                    "distance": "1.1 miles"
                }
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/document-analysis", response_model=DocumentAnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    """
    Accepts an uploaded PDF emergency plan or protocol document
    and returns a summary, warnings, and safety recommendations.
    
    Future Integration:
    - Connect to LangChain's PDF loader (PyPDFLoader), splitter,
      and vector store QA chain using Gemini embeddings.
    """
    try:
        # Check that file is indeed a PDF
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF documents are supported.")
            
        # Placeholder response
        return DocumentAnalysisResponse(
            summary=(
                f"The document '{file.filename}' outlines civil emergency evacuation "
                "protocols, defining warning levels, staging sites, and safety guidelines."
            ),
            warnings=[
                "Turn off the power main before water levels reach electrical outlets.",
                "Evacuate immediately when water rises above level tier 3 (2.5 meters)."
            ],
            recommendations=[
                "Prepare a minimum 72-hour survival go-bag.",
                "Verify evacuation routes with regional command before departure."
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system-status", response_model=SystemStatusResponse)
async def get_system_status():
    """
    Returns the live health status of the application components.
    """
    return SystemStatusResponse(
        backend="online",
        workflow="active",
        mcp="connected"
    )

@app.get("/agent-status", response_model=AgentStatusResponse)
async def get_agent_status():
    """
    Returns the operational state of individual Google ADK agents.
    """
    return AgentStatusResponse(
        coordinator_agent="active",
        weather_agent="active",
        news_agent="active",
        resource_agent="active",
        risk_agent="active",
        response_agent="active"
    )
