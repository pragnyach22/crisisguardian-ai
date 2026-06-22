# CrisisGuardian AI - Architecture Documentation

CrisisGuardian AI is a premium multi-agent disaster response assistant designed to deliver high-quality, actionable, and rapid instructions during physical threats like floods, cyclones, earthquakes, and fires.

## System Topology

```mermaid
graph TD
    User([Citizen/User]) -->|Interact| Streamlit[Streamlit Frontend]
    Streamlit -->|HTTP POST /api/chat| FastAPI[FastAPI Backend]
    FastAPI -->|Invoke State| LangGraph[LangGraph Coordinator]
    
    subgraph Multi-Agent Hub
        LangGraph -->|Routes| Supervisor[Emergency Supervisor Node]
        Supervisor -->|Delegates| FloodAgent[Flood Specialist]
        Supervisor -->|Delegates| CycloneAgent[Cyclone Specialist]
        Supervisor -->|Delegates| EarthquakeAgent[Earthquake Specialist]
        Supervisor -->|Delegates| FireAgent[Fire Specialist]
    end
    
    subgraph Extensible Tools
        FloodAgent --> Tools[Disaster Tools API]
        CycloneAgent --> Tools
        EarthquakeAgent --> Tools
        FireAgent --> Tools
        
        Tools --> Weather[Weather Alerts API]
        Tools --> Seismic[USGS Earthquake Query]
        Tools --> Shelter[Shelter Locator]
        Tools --> SOS[Emergency Rescue Dispatch]
    end
    
    Multi-Agent Hub -->|LLM Reasoning| Gemini[Gemini 2.5 Flash]
```

## Module Architecture

### 1. Base Agent Framework (`agents/base_agent.py`)
- Employs `ChatGoogleGenerativeAI` wrapper powered by the `gemini-2.5-flash` model.
- Standardizes parameter settings (default temperature of 0.2 for precise, fact-based response generation).
- Creates prompt configurations dividing instruction levels between system prompts and user parameters.

### 2. Specialized Disaster Agents (`agents/disaster_agents.py`)
- **FloodResponseAgent**: Focused on route safety, vertical evacuation directives, utility mitigation, and sanitation rules.
- **CycloneResponseAgent**: Specialized in window protection, storm shelters, immediate tracking, and post-storm danger warnings.
- **EarthquakeResponseAgent**: Governs Drop-Cover-Hold rules, outdoor open area guidelines, and aftershock safety procedures.
- **FireResponseAgent**: Instructs on escape pathing (smoke navigation), wildfire structural clearance, and immediate evacuation protocols.
- **EmergencySupervisorAgent**: Acts as a state dispatcher, classifying initial requests, determining which agent to call, and handling general emergency inquiries.

### 3. Integrated State Machine Workflows (`workflows/disaster_workflow.py`)
- Powered by `LangGraph` defining node state components including active messages, disaster class state, coordinates, and final response.
- Includes a conditional routing edge mapping supervisor node routing parameters directly to specialized target agents.

### 4. Custom API Tools (`tools/disaster_tools.py`)
- Leverages the LangChain `@tool` decorator structure.
- **Weather Alerts**: Fetches mock warning advisories for localized areas.
- **Earthquake Alerts**: Connects live to the USGS geojson feed to fetch recent magnitude 4.0+ events.
- **Shelter Search**: Resolves locations to lists of available high-safety community shelter spots.
- **SOS Alerting**: Simulated dispatcher notifying local emergency services.

### 5. Backend Server API (`backend/app.py`)
- FastAPI service layer running locally on Uvicorn.
- CORS-enabled routes supporting multi-origin client requests.
- Runs the active LangGraph flow, falling back to mock routing simulations if `GEMINI_API_KEY` is not present in `.env`.
