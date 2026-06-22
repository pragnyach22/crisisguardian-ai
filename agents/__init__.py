"""
CrisisGuardian AI Agents Package
Defines the base agent architecture, specialized disaster response agents,
and the new Google ADK-style agent skeletons.
"""

from .base_agent import BaseDisasterAgent
from .disaster_agents import (
    FloodAgent,
    CycloneAgent,
    EarthquakeAgent,
    FireAgent,
    EmergencySupervisorAgent
)

# Import the Google ADK Agents
from .coordinator_agent import coordinator_agent
from .weather_agent import weather_agent
from .news_agent import news_agent
from .resource_agent import resource_agent
from .risk_agent import risk_agent
from .response_agent import response_agent

__all__ = [
    "BaseDisasterAgent",
    "FloodAgent",
    "CycloneAgent",
    "EarthquakeAgent",
    "FireAgent",
    "EmergencySupervisorAgent",
    "coordinator_agent",
    "weather_agent",
    "news_agent",
    "resource_agent",
    "risk_agent",
    "response_agent"
]

