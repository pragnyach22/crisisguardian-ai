"""
CrisisGuardian AI - Sequential Crisis Workflow (LangGraph)
===========================================================
Defines the multi-agent execution pipeline passing information through:
START -> Coordinator -> Weather -> News -> Resource -> Risk -> Response -> END
"""

from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END

# 1. State Definition
class CrisisWorkflowState(TypedDict):
    """
    State contract defining data propagated across the emergency agents.
    """
    messages: List[BaseMessage]
    location: str
    crisis_type: str                   # 'flood', 'cyclone', 'earthquake', 'fire', 'general'
    
    # Data gathered along the pipeline
    weather_data: Optional[Dict[str, Any]]
    news_data: Optional[List[Dict[str, Any]]]
    resource_data: Optional[List[Dict[str, Any]]]
    risk_level: Optional[str]          # 'Low', 'Moderate', 'High', 'Extreme'
    
    # Final guidance report generated
    final_guidance: Optional[str]

import logging

# Configure logger
logger = logging.getLogger("CrisisWorkflow")

# Import the Google ADK Agents
from agents.coordinator_agent import coordinator_agent
from agents.weather_agent import weather_agent
from agents.news_agent import news_agent
from agents.resource_agent import resource_agent
from agents.risk_agent import risk_agent
from agents.response_agent import response_agent

# 2. Node Implementations (Agent Execution Steps)
def coordinator_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Coordinator Agent.
    Receives user query, initializes settings, and determines target locations.
    """
    logger.info("Executing Coordinator Agent - Parsing query and setting context...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    location = state.get("location") or ""
    
    # Extract location if not explicitly provided in the state context
    if not location and last_message:
        last_message_lower = last_message.lower()
        if "andhra pradesh" in last_message_lower or "ap" in last_message_lower:
            location = "Andhra Pradesh"
        elif "mumbai" in last_message_lower:
            location = "Mumbai"
        else:
            location = "General Coastal Region"
            
    crisis_type = state.get("crisis_type") or "general"
    
    return {
        "location": location,
        "crisis_type": crisis_type
    }

def weather_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Weather Agent.
    Fetches forecasting warnings and weather alerts.
    """
    logger.info("Executing Weather Agent - Fetching forecasting details...")
    
    # =========================================================================
    # FUTURE MCP WEATHER INTEGRATION:
    # weather_data = weather_agent.run(...) using tools.weather_tool
    # =========================================================================
    weather_data = {
        "condition": "Severe rain forecast with flash flood watch",
        "wind_speed": "75 km/h",
        "precipitation_rate": "15mm/hr",
        "source": "WeatherAgent (Meteorological Feed)"
    }
    
    return {
        "weather_data": weather_data
    }

def news_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the News Agent.
    Fetches civil notifications and official announcements.
    """
    logger.info("Executing News Agent - Fetching emergency civil defense bulletins...")
    
    # =========================================================================
    # FUTURE MCP NEWS INTEGRATION:
    # news_data = news_agent.run(...) using tools.news_tool
    # =========================================================================
    news_data = [
        {
            "headline": "Evacuation order declared for low-lying zones.",
            "source": "Civil Defense Authority"
        }
    ]
    
    return {
        "news_data": news_data
    }

def resource_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Resource Agent.
    Locates emergency facilities, shelter houses, and dispatch command centers.
    """
    logger.info("Executing Resource Agent - Querying shelters and clinics...")
    
    # =========================================================================
    # FUTURE MCP RESOURCE INTEGRATION:
    # resource_data = resource_agent.run(...) using tools.resource_tool
    # =========================================================================
    resource_data = [
        {
            "name": "Cyclone Refuge Center B",
            "distance": "0.9 miles",
            "status": "Open"
        }
    ]
    
    return {
        "resource_data": resource_data
    }

def risk_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Risk Agent.
    Computes threat level based on consolidated data inputs.
    """
    logger.info("Executing Risk Agent - Running composite safety evaluation index...")
    
    # =========================================================================
    # FUTURE INTEGRATION:
    # risk_level = risk_agent.run(...) using composite calculation matrices
    # =========================================================================
    risk_level = "High"
    
    return {
        "risk_level": risk_level
    }

def response_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Response Agent.
    Generates step-by-step guidance checklists and final action items.
    """
    logger.info("Executing Response Agent - Formulating safety guidelines checklist...")
    
    # =========================================================================
    # FUTURE INTEGRATION:
    # final_guidance = response_agent.run(...) synthesizing gathered state
    # =========================================================================
    location = state.get("location") or "General Region"
    final_guidance = (
        f"EMERGENCY DIRECTIVE FOR {location.upper()}: "
        "A flash flood watch is active. Local alerts verify severe wind vectors. "
        "Evacuate to Cyclone Refuge Center B (0.9 miles away). Stay indoors, "
        "charge communication devices, and keep emergency supplies ready."
    )
    
    return {
        "final_guidance": final_guidance
    }


# 3. Assemble StateGraph
def create_crisis_workflow() -> StateGraph:
    """
    Creates and compiles the StateGraph workflow connecting the nodes sequentially.
    """
    # Create workflow graph matching state
    builder = StateGraph(CrisisWorkflowState)
    
    # Add nodes
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("weather", weather_node)
    builder.add_node("news", news_node)
    builder.add_node("resource", resource_node)
    builder.add_node("risk", risk_node)
    builder.add_node("response", response_node)
    
    # Add sequential edges
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "weather")
    builder.add_edge("weather", "news")
    builder.add_edge("news", "resource")
    builder.add_edge("resource", "risk")
    builder.add_edge("risk", "response")
    builder.add_edge("response", END)
    
    # Compile graph ready for invoke
    return builder.compile()

# Instantiated workflow for direct usage
crisis_workflow = create_crisis_workflow()
