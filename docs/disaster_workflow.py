"""
CrisisGuardian AI - Disaster Response Workflow (LangGraph)
Uses LangGraph to define a stateful multi-agent system orchestrating disaster response.
The supervisor routes the user query to the appropriate agent.
"""

from typing import Annotated, TypedDict, Sequence, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

# Import our specialized agents
from agents.disaster_agents import (
    FloodAgent,
    CycloneAgent,
    EarthquakeAgent,
    FireAgent,
    EmergencySupervisorAgent
)

# 1. State Definition
class DisasterWorkflowState(TypedDict):
    """
    State representing the context of a disaster query conversation.
    """
    messages: Sequence[BaseMessage]
    current_crisis_type: str        # 'flood', 'cyclone', 'earthquake', 'fire', 'general'
    location: str
    next_node: str                  # Routes execution flow
    output: Dict[str, Any]          # Summary output of response

# 2. Node Implementations
def supervisor_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    """
    Supervisor Agent evaluates user input and decides which agent should respond.
    """
    supervisor = EmergencySupervisorAgent()
    last_message = state["messages"][-1].content
    
    # We can perform classification logic or utilize LLM to route.
    # For boilerplate correctness, we evaluate keywords or delegate via a small LLM call.
    content_lower = last_message.lower()
    
    next_node = "general"
    crisis_type = "general"
    
    if "flood" in content_lower or "water" in content_lower or "rain" in content_lower:
        next_node = "flood"
        crisis_type = "flood"
    elif "cyclone" in content_lower or "hurricane" in content_lower or "wind" in content_lower or "storm" in content_lower:
        next_node = "cyclone"
        crisis_type = "cyclone"
    elif "earthquake" in content_lower or "tremor" in content_lower or "quake" in content_lower:
        next_node = "earthquake"
        crisis_type = "earthquake"
    elif "fire" in content_lower or "smoke" in content_lower or "burn" in content_lower:
        next_node = "fire"
        crisis_type = "fire"
        
    return {
        "next_node": next_node,
        "current_crisis_type": crisis_type
    }

def flood_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    agent = FloodAgent()
    last_message = state["messages"][-1].content
    
    # Get prompt chain and run
    runnable = agent.get_runnable("Respond to the user request. Context: user location is {location}.\nRequest: {input}")
    response = runnable.invoke({
        "location": state.get("location", "unknown location"),
        "input": last_message
    })
    
    return {
        "messages": [AIMessage(content=response.content, name="FloodResponseAgent")],
        "output": {
            "agent_name": "FloodResponseAgent",
            "response": response.content,
            "recommended_actions": [
                "Seek high ground immediately.",
                "Avoid walking or driving through floodwaters.",
                "Turn off utilities and prepare drinking water."
            ]
        }
    }

def cyclone_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    agent = CycloneAgent()
    last_message = state["messages"][-1].content
    
    runnable = agent.get_runnable("Respond to the user request. Context: user location is {location}.\nRequest: {input}")
    response = runnable.invoke({
        "location": state.get("location", "unknown location"),
        "input": last_message
    })
    
    return {
        "messages": [AIMessage(content=response.content, name="CycloneResponseAgent")],
        "output": {
            "agent_name": "CycloneResponseAgent",
            "response": response.content,
            "recommended_actions": [
                "Stay indoors in a windowless room.",
                "Ensure emergency radios and flashlights have working batteries.",
                "Secure loose items outside the house."
            ]
        }
    }

def earthquake_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    agent = EarthquakeAgent()
    last_message = state["messages"][-1].content
    
    runnable = agent.get_runnable("Respond to the user request. Context: user location is {location}.\nRequest: {input}")
    response = runnable.invoke({
        "location": state.get("location", "unknown location"),
        "input": last_message
    })
    
    return {
        "messages": [AIMessage(content=response.content, name="EarthquakeResponseAgent")],
        "output": {
            "agent_name": "EarthquakeResponseAgent",
            "response": response.content,
            "recommended_actions": [
                "Drop, Cover, and Hold On.",
                "Move away from windows and glass structures.",
                "Be alert for potential aftershocks."
            ]
        }
    }

def fire_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    agent = FireAgent()
    last_message = state["messages"][-1].content
    
    runnable = agent.get_runnable("Respond to the user request. Context: user location is {location}.\nRequest: {input}")
    response = runnable.invoke({
        "location": state.get("location", "unknown location"),
        "input": last_message
    })
    
    return {
        "messages": [AIMessage(content=response.content, name="FireResponseAgent")],
        "output": {
            "agent_name": "FireResponseAgent",
            "response": response.content,
            "recommended_actions": [
                "Stay low to the ground to avoid inhaling toxic smoke.",
                "Check door handles for heat before opening.",
                "Evacuate following predefined exit routes."
            ]
        }
    }

def general_node(state: DisasterWorkflowState) -> Dict[str, Any]:
    agent = EmergencySupervisorAgent()
    last_message = state["messages"][-1].content
    
    runnable = agent.get_runnable("Answer the general emergency query or provide assistance. Location: {location}.\nQuery: {input}")
    response = runnable.invoke({
        "location": state.get("location", "unknown location"),
        "input": last_message
    })
    
    return {
        "messages": [AIMessage(content=response.content, name="EmergencySupervisorAgent")],
        "output": {
            "agent_name": "EmergencySupervisorAgent",
            "response": response.content,
            "recommended_actions": [
                "Assess the situation and contact local emergency dispatch (e.g. 911 / 112).",
                "Ensure physical safety before seeking information.",
                "Keep emergency equipment ready."
            ]
        }
    }

# 3. Router logic
def router_edge(state: DisasterWorkflowState) -> str:
    """
    Decides routing based on the state's next_node value set by the supervisor.
    """
    target = state.get("next_node", "general")
    if target in ["flood", "cyclone", "earthquake", "fire"]:
        return target
    return "general"

# 4. Build LangGraph Workflow
def create_disaster_workflow():
    workflow = StateGraph(DisasterWorkflowState)
    
    # Register Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("flood", flood_node)
    workflow.add_node("cyclone", cyclone_node)
    workflow.add_node("earthquake", earthquake_node)
    workflow.add_node("fire", fire_node)
    workflow.add_node("general", general_node)
    
    # Establish entry point
    workflow.set_entry_point("supervisor")
    
    # Add conditional routing edges
    workflow.add_conditional_edges(
        "supervisor",
        router_edge,
        {
            "flood": "flood",
            "cyclone": "cyclone",
            "earthquake": "earthquake",
            "fire": "fire",
            "general": "general"
        }
    )
    
    # Connect leaf nodes to END
    workflow.add_edge("flood", END)
    workflow.add_edge("cyclone", END)
    workflow.add_edge("earthquake", END)
    workflow.add_edge("fire", END)
    workflow.add_edge("general", END)
    
    # Compile graph
    return workflow.compile()
