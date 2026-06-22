"""
CrisisGuardian AI - Coordinator Agent
=====================================
Responsibility:
- Receives initial user requests regarding emergency situations.
- Orchestrates tasks and delegates processing to specialized agents (Weather, News, Resource, Risk, Response).
- Coordinates state updates and multi-agent task execution.
"""

import logging
from google.adk.agents import Agent

# Import specialized agents (relative imports to avoid circular/redundant package lookups)
from .weather_agent import weather_agent
from .news_agent import news_agent
from .resource_agent import resource_agent
from .risk_agent import risk_agent
from .response_agent import response_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("CoordinatorAgent")

# Initialize the Google ADK Coordinator Agent instance
coordinator_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the CrisisGuardian AI Emergency Coordinator. Your responsibilities are:\n"
        "1. Receive the initial user query or distress signal.\n"
        "2. Parse the request to extract location and disaster details.\n"
        "3. Delegate specific queries to the Weather Agent, News Agent, Resource Agent, and Risk Agent.\n"
        "4. Synthesize the inputs and route them to the Response Agent for final instructions.\n"
        "Do not make up disaster reports; rely entirely on facts returned by specialized agents and tools."
    )
)

def delegate_crisis_tasks(event: dict) -> dict:
    """
    Orchestrates the multi-agent task execution flow.
    - Receives user query.
    - Extracts location.
    - Calls Weather Agent.
    - Calls News Agent.
    - Calls Resource Agent.
    - Calls Risk Agent.
    - Sends gathered information to Response Agent.
    - Returns structured results dictionary.
    
    Args:
        event (dict): Incoming dict containing user "query" and optional "location".
        
    Returns:
        dict: The structured analysis response.
    """
    query = event.get("query", "")
    location = event.get("location", "")
    
    logger.info("Executing Coordinator Agent - Parsing query and extracting parameters...")
    
    # Extract location if not explicitly provided
    if not location:
        query_lower = query.lower()
        if "andhra pradesh" in query_lower or "ap" in query_lower:
            location = "Andhra Pradesh"
        elif "mumbai" in query_lower:
            location = "Mumbai"
        else:
            location = "General Coastal Region"
    
    logger.info(f"Coordinator resolved location parameter: '{location}'")
    
    # 1. WEATHER AGENT
    logger.info("Triggering Weather Agent node execution...")
    # =========================================================================
    # FUTURE MCP WEATHER TOOL INTEGRATION:
    # Instead of mock return dicts, call the weather agent's weather_tool:
    #   from tools.weather_tool import WeatherTool
    #   wt = WeatherTool()
    #   weather_data = wt.get_weather_alerts(location)
    # =========================================================================
    weather_result = {
        "condition": "Severe rain forecast with flash flood watch",
        "wind_speed": "75 km/h",
        "precipitation_rate": "15mm/hr",
        "source": "WeatherAgent (Meteorological Feed)"
    }
    
    # 2. NEWS AGENT
    logger.info("Triggering News Agent node execution...")
    # =========================================================================
    # FUTURE MCP NEWS TOOL INTEGRATION:
    # Call the news agent's news_tool to find municipal hazard notices:
    #   from tools.news_tool import NewsTool
    #   nt = NewsTool()
    #   news_data = nt.fetch_emergency_broadcasts(location)
    # =========================================================================
    news_result = {
        "active_warnings": [
            "Mandatory evacuation ordered for Zone A (coastal strips)",
            "District collector orders closing of harbor docks"
        ],
        "source": "NewsAgent (Emergency Civil Broadcast)"
    }
    
    # 3. RESOURCE AGENT
    logger.info("Triggering Resource Agent node execution...")
    # =========================================================================
    # FUTURE MCP RESOURCE TOOL INTEGRATION:
    # Call the resource agent's resource_tool to fetch coordinates:
    #   from tools.resource_tool import ResourceTool
    #   rt = ResourceTool()
    #   resources = rt.find_shelters(location)
    # =========================================================================
    resources_result = {
        "hospitals": [
            {"name": "District Health Center Clinic", "distance": "1.2 miles", "status": "Active Capacity"}
        ],
        "shelters": [
            {"name": "Cyclone Refuge Center B", "distance": "0.9 miles", "status": "Open"}
        ],
        "police_stations": [
            {"name": "Coastal Safety Police Unit", "distance": "2.1 miles", "status": "Patrol Active"}
        ],
        "fire_stations": [
            {"name": "Metro Fire Station 4", "distance": "1.4 miles", "status": "Ready"}
        ]
    }
    
    # 4. RISK AGENT
    logger.info("Triggering Risk Agent node execution...")
    # =========================================================================
    # FUTURE INTEGRATION:
    # Calculate composite danger scales based on weather + news vectors:
    #   risk_score = risk_agent.run(...)
    # =========================================================================
    risk_level = "HIGH"
    
    # 5. RESPONSE AGENT
    logger.info("Triggering Response Agent node execution...")
    # =========================================================================
    # FUTURE INTEGRATION:
    # Compile the final safety report for presentation:
    #   final_guidance = response_agent.run(...)
    # =========================================================================
    final_response = (
        f"EMERGENCY DIRECTIVE FOR {location.upper()}: "
        "A flash flood watch is active. Local alerts verify severe wind vectors. "
        "Evacuate to Cyclone Refuge Center B (0.9 miles away). Stay indoors, "
        "charge communication devices, and keep emergency supplies ready."
    )
    
    # Build structured response matching layout specs
    structured_response = {
        "weather": weather_result,
        "news": news_result,
        "resources": resources_result,
        "risk_level": risk_level,
        "final_response": final_response
    }
    
    logger.info("Multi-agent task delegation successfully compiled.")
    return structured_response
