"""
CrisisGuardian AI - Unit Tests
Tests for agents, tools, and workflow components.
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set mock API key for testing
os.environ["GEMINI_API_KEY"] = "test_key_12345"


# =========================================================================
# TEST: Base Agent
# =========================================================================

class TestBaseDisasterAgent:
    """Tests for BaseDisasterAgent class."""
    
    def test_agent_initialization(self):
        """Test that agent initializes without errors."""
        from agents.base_agent import BaseDisasterAgent
        
        agent = BaseDisasterAgent(
            agent_name="TestAgent",
            system_instruction="Test instruction"
        )
        
        assert agent.agent_name == "TestAgent"
        assert agent.temperature == 0.2
    
    def test_agent_prompt_creation(self):
        """Test prompt creation."""
        from agents.base_agent import BaseDisasterAgent
        
        agent = BaseDisasterAgent(
            agent_name="TestAgent",
            system_instruction="You are a test agent."
        )
        
        prompt = agent._create_prompt("Hello, what should I do?")
        assert prompt is not None


# =========================================================================
# TEST: Disaster Agents
# =========================================================================

class TestDisasterAgents:
    """Tests for specialized disaster agents."""
    
    def test_flood_agent_creation(self):
        """Test FloodAgent initialization."""
        from agents.disaster_agents import FloodAgent
        
        agent = FloodAgent()
        assert agent.agent_name == "FloodResponseAgent"
        assert "flood" in agent.system_instruction.lower()
    
    def test_cyclone_agent_creation(self):
        """Test CycloneAgent initialization."""
        from agents.disaster_agents import CycloneAgent
        
        agent = CycloneAgent()
        assert agent.agent_name == "CycloneResponseAgent"
        assert "cyclone" in agent.system_instruction.lower()
    
    def test_earthquake_agent_creation(self):
        """Test EarthquakeAgent initialization."""
        from agents.disaster_agents import EarthquakeAgent
        
        agent = EarthquakeAgent()
        assert agent.agent_name == "EarthquakeResponseAgent"
        assert "earthquake" in agent.system_instruction.lower()
    
    def test_fire_agent_creation(self):
        """Test FireAgent initialization."""
        from agents.disaster_agents import FireAgent
        
        agent = FireAgent()
        assert agent.agent_name == "FireResponseAgent"
        assert "fire" in agent.system_instruction.lower()
    
    def test_supervisor_agent_creation(self):
        """Test EmergencySupervisorAgent initialization."""
        from agents.disaster_agents import EmergencySupervisorAgent
        
        agent = EmergencySupervisorAgent()
        assert agent.agent_name == "EmergencySupervisorAgent"
        assert "supervisor" in agent.system_instruction.lower()


# =========================================================================
# TEST: Weather Tool
# =========================================================================

class TestWeatherTool:
    """Tests for WeatherTool."""
    
    def test_weather_tool_initialization(self):
        """Test WeatherTool initialization."""
        from tools.weather_tool import WeatherTool
        
        tool = WeatherTool()
        assert tool is not None
    
    def test_mock_weather_response(self):
        """Test mock weather response."""
        from tools.weather_tool import WeatherTool
        
        tool = WeatherTool(api_key="invalid_key")
        weather = tool.get_current_weather("Mumbai")
        
        assert "location" in weather
        assert "temperature_c" in weather
        assert "condition" in weather
    
    def test_weather_alerts(self):
        """Test weather alerts generation."""
        from tools.weather_tool import WeatherTool
        
        tool = WeatherTool()
        alerts = tool.get_weather_alerts("Mumbai")
        
        assert isinstance(alerts, list)


# =========================================================================
# TEST: News Tool
# =========================================================================

class TestNewsTool:
    """Tests for NewsTool."""
    
    def test_news_tool_initialization(self):
        """Test NewsTool initialization."""
        from tools.news_tool import NewsTool
        
        tool = NewsTool()
        assert tool is not None
    
    def test_fetch_disaster_news(self):
        """Test news fetching."""
        from tools.news_tool import NewsTool
        
        tool = NewsTool()
        news = tool.fetch_disaster_news("Mumbai", "flood")
        
        assert isinstance(news, list)
        if news:
            assert "headline" in news[0]
    
    def test_emergency_broadcasts(self):
        """Test emergency broadcast fetching."""
        from tools.news_tool import NewsTool
        
        tool = NewsTool()
        broadcasts = tool.fetch_emergency_broadcasts("Mumbai")
        
        assert isinstance(broadcasts, list)


# =========================================================================
# TEST: Resource Tool
# =========================================================================

class TestResourceTool:
    """Tests for ResourceTool."""
    
    def test_resource_tool_initialization(self):
        """Test ResourceTool initialization."""
        from tools.resource_tool import ResourceTool
        
        tool = ResourceTool()
        assert tool is not None
    
    def test_find_shelters(self):
        """Test shelter finding."""
        from tools.resource_tool import ResourceTool
        
        tool = ResourceTool()
        shelters = tool.find_shelters("Mumbai")
        
        assert isinstance(shelters, list)
    
    def test_find_hospitals(self):
        """Test hospital finding."""
        from tools.resource_tool import ResourceTool
        
        tool = ResourceTool()
        hospitals = tool.find_hospitals("Mumbai")
        
        assert isinstance(hospitals, list)
    
    def test_find_emergency_services(self):
        """Test emergency services finding."""
        from tools.resource_tool import ResourceTool
        
        tool = ResourceTool()
        services = tool.find_emergency_services("Mumbai")
        
        assert isinstance(services, list)


# =========================================================================
# TEST: Disaster Tools
# =========================================================================

class TestDisasterTools:
    """Tests for disaster tools."""
    
    def test_weather_alerts_tool(self):
        """Test weather alerts tool."""
        from tools.disaster_tools import get_weather_alerts
        
        result = get_weather_alerts("Mumbai")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_earthquake_alerts_tool(self):
        """Test earthquake alerts tool."""
        from tools.disaster_tools import get_earthquake_alerts
        
        result = get_earthquake_alerts(5.0)
        assert isinstance(result, str)
    
    def test_find_nearest_shelter_tool(self):
        """Test shelter finder tool."""
        from tools.disaster_tools import find_nearest_shelter
        
        result = find_nearest_shelter("Mumbai", "flood")
        assert isinstance(result, str)
        assert "shelter" in result.lower() or "miles" in result.lower()
    
    def test_sos_notification_tool(self):
        """Test SOS notification tool."""
        from tools.disaster_tools import send_sos_notification
        
        result = send_sos_notification("user123", "19.0760,72.8777", "Flood emergency")
        assert "SOS" in result or "dispatch" in result.lower()


# =========================================================================
# TEST: Crisis Workflow
# =========================================================================

class TestCrisisWorkflow:
    """Tests for crisis workflow."""
    
    def test_workflow_creation(self):
        """Test workflow graph creation."""
        from workflows.crisis_workflow import create_crisis_workflow
        
        workflow = create_crisis_workflow()
        assert workflow is not None
    
    @pytest.mark.skip(reason="Requires Gemini API or full mock setup")
    def test_coordinator_node(self):
        """Test coordinator node."""
        from workflows.crisis_workflow import coordinator_node, CrisisWorkflowState
        from langchain_core.messages import HumanMessage
        
        state = CrisisWorkflowState(
            messages=[HumanMessage(content="Flood in Mumbai")],
            location="unknown",
            crisis_type="general",
            weather_data=None,
            news_data=None,
            resource_data=None,
            risk_level=None,
            risk_score=None,
            risk_reason=None,
            checklist=None,
            final_guidance=None,
            monitoring_data=None
        )
        
        result = coordinator_node(state)
        assert "location" in result or "crisis_type" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
