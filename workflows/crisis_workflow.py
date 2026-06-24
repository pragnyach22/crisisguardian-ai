"""
CrisisGuardian AI - Sequential Crisis Workflow (LangGraph)
===========================================================
Defines the multi-agent execution pipeline passing information through:
START -> Coordinator -> Weather -> News -> Resource -> Risk -> Response -> Checklist -> END
"""

import os
import time
import logging
import json
from datetime import datetime
from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("CrisisWorkflow")

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
    resource_data: Optional[Dict[str, Any]]
    risk_level: Optional[str]          # 'Low', 'Moderate', 'High', 'Critical'
    risk_score: Optional[int]          # 1-10
    risk_reason: Optional[str]         # Detailed explanation
    
    # Final guidance report and checklist
    checklist: Optional[List[str]]
    final_guidance: Optional[str]

    # Telemetry monitoring data
    monitoring_data: Optional[Dict[str, Any]]


def log_node_telemetry(node_name: str, state: CrisisWorkflowState, status: str, start_time: float, error_msg: str = None) -> Dict[str, Any]:
    """
    Utility to record node execution metrics in the state monitoring dictionary.
    """
    end_time = time.time()
    exec_time_ms = round((end_time - start_time) * 1000, 2)
    start_dt = datetime.fromtimestamp(start_time).strftime("%H:%M:%S.%f")[:-3]
    end_dt = datetime.fromtimestamp(end_time).strftime("%H:%M:%S.%f")[:-3]
    
    monitoring_data = state.get("monitoring_data") or {}
    monitoring_data[node_name] = {
        "status": status,
        "start_time": start_dt,
        "end_time": end_dt,
        "exec_time": f"{exec_time_ms} ms",
        "exec_time_ms": exec_time_ms,
        "success": status == "Completed",
        "error": error_msg
    }
    return monitoring_data


def _score_to_risk_level(score: int) -> str:
    """Maps a 1-10 risk score to a threat tier label."""
    if score >= 9:
        return "Critical"
    if score >= 7:
        return "High"
    if score >= 4:
        return "Moderate"
    return "Low"


def _compute_risk_assessment(
    disaster_type: str,
    weather: Dict[str, Any],
    news: Optional[List[Dict[str, Any]]] = None,
) -> tuple[int, str, str]:
    """
    Rule-based risk scoring aligned to the active crisis type.
    Prevents location-based mock weather from inflating unrelated queries.
    """
    disaster_type = (disaster_type or "general").lower()
    weather_curr = weather.get("current", {}) if weather else {}
    cond = str(weather_curr.get("condition", "")).lower()
    wind = float(weather_curr.get("wind_speed_kmh", 0) or 0)
    alerts = weather.get("alerts", []) if weather else []
    news = news or []

    base_scores = {
        "general": 2,
        "fire": 5,
        "flood": 5,
        "earthquake": 6,
        "cyclone": 6,
    }
    score = base_scores.get(disaster_type, 3)
    reasons = []

    if disaster_type == "cyclone":
        if "cyclone" in cond or wind >= 62:
            score += 3
            reasons.append(f"cyclonic conditions with {wind} km/h winds")
        elif wind >= 40:
            score += 1
            reasons.append("elevated wind speeds near coast")
        else:
            reasons.append("cyclone inquiry with no extreme wind readings yet")
    elif disaster_type == "flood":
        if "rain" in cond or "thunderstorm" in cond or "flood" in cond:
            score += 2
            reasons.append("heavy rainfall increasing flood risk")
        else:
            reasons.append("flood-related inquiry without active rainfall")
    elif disaster_type == "earthquake":
        score += 1 if news else 0
        reasons.append("seismic event reported" if news else "earthquake preparedness context")
    elif disaster_type == "fire":
        if wind >= 30 or "clear" in cond:
            score += 1
            reasons.append("dry or windy conditions may spread fire")
        else:
            reasons.append("fire safety inquiry")
    else:
        score = min(score, 3)
        if alerts:
            score += 1
            reasons.append("minor weather advisories present")
        else:
            reasons.append("general preparedness — no active emergency detected")

    if disaster_type != "general" and len(news) >= 2:
        score += 1
        reasons.append("multiple official bulletins corroborate the threat")

    score = max(1, min(10, score))
    level = _score_to_risk_level(score)
    reason = "; ".join(reasons) + f". Assessed tier: {level} ({score}/10)."
    return score, level, reason


# 2. Node Implementations (Agent Execution Steps)
def coordinator_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Coordinator Agent.
    Parses location and disaster details from user query using Gemini.
    """
    start_time = time.time()
    logger.info("Executing Coordinator Agent...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    location = state.get("location") or ""
    disaster_type = state.get("crisis_type") or "general"
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, google_api_key=api_key)
            prompt = (
                f"Extract the target location and disaster type from this query: '{last_message}'. "
                "Return ONLY a valid JSON object in the format: "
                "{\"location\": \"extracted location\", \"disaster_type\": \"flood|cyclone|earthquake|fire|general\"}. "
                "Do not include markdown tags like ```json or anything else. Just the raw JSON string."
            )
            response = llm.invoke(prompt)
            clean_res = response.content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_res)
            
            if data.get("location"):
                location = data.get("location")
            if data.get("disaster_type"):
                disaster_type = data.get("disaster_type")
        except Exception as e:
            logger.error(f"Coordinator LLM call failed: {e}")
            
    # Simple regex fallback if location or disaster_type is still default/empty
    if not location or location == "unknown location" or location == "General Region":
        query_lower = last_message.lower()
        if "andhra" in query_lower or "ap" in query_lower or "visakhapatnam" in query_lower:
            location = "Andhra Pradesh"
        elif "mumbai" in query_lower:
            location = "Mumbai"
        else:
            location = "General Region"
            
    if not disaster_type or disaster_type == "general":
        query_lower = last_message.lower()
        if "flood" in query_lower or "water" in query_lower or "rain" in query_lower:
            disaster_type = "flood"
        elif "cyclone" in query_lower or "hurricane" in query_lower or "wind" in query_lower or "storm" in query_lower:
            disaster_type = "cyclone"
        elif "earthquake" in query_lower or "tremor" in query_lower or "quake" in query_lower:
            disaster_type = "earthquake"
        elif "fire" in query_lower or "smoke" in query_lower or "burn" in query_lower:
            disaster_type = "fire"
        else:
            disaster_type = "general"

    logger.info(f"Coordinator parsed parameters -> Location: {location}, Crisis: {disaster_type}")
    
    # Log telemetry
    mon = log_node_telemetry("Coordinator Agent", state, "Completed", start_time)
    
    return {
        "location": location,
        "crisis_type": disaster_type,
        "monitoring_data": mon
    }

def weather_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Weather Agent.
    Fetches real OpenWeatherMap readings and triggers alert warnings.
    """
    start_time = time.time()
    logger.info("Executing Weather Agent...")
    location = state.get("location") or "General Region"
    crisis_type = state.get("crisis_type") or "general"
    
    try:
        from tools.weather_tool import WeatherTool
        wt = WeatherTool()
        current = wt.get_current_weather(location, crisis_type)
        alerts = wt.get_weather_alerts(location, crisis_type)
        weather_data = {
            "current": current,
            "alerts": alerts,
            "source": "OpenWeatherMap API"
        }
        mon = log_node_telemetry("Weather Agent", state, "Completed", start_time)
    except Exception as e:
        logger.error(f"Weather Agent node error: {e}")
        weather_data = {
            "current": {"condition": "Cloudy", "temperature_c": 24.0, "humidity": 60, "wind_speed_kmh": 15.0},
            "alerts": [],
            "source": "Mock Fallback Feed"
        }
        mon = log_node_telemetry("Weather Agent", state, "Failed", start_time, str(e))
        
    return {
        "weather_data": weather_data,
        "monitoring_data": mon
    }

def news_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the News Agent.
    Fetches civil warnings and announcements.
    """
    start_time = time.time()
    logger.info("Executing News Agent...")
    location = state.get("location") or "General Region"
    crisis_type = state.get("crisis_type") or "general"
    
    try:
        from tools.news_tool import NewsTool
        nt = NewsTool()
        news = nt.fetch_disaster_news(location, crisis_type)
        broadcasts = nt.fetch_emergency_broadcasts(location)
        
        merged_news = []
        for n in news:
            merged_news.append({
                "headline": n.get("headline"),
                "source": n.get("source", "Emergency Bulletin"),
                "summary": n.get("summary")
            })
        for b in broadcasts:
            merged_news.append({
                "headline": f"ALERT: {b.get('type')} in {b.get('target_area')}",
                "source": b.get("agency", "Civil Defense Bureau"),
                "summary": b.get("instruction")
            })
            
        mon = log_node_telemetry("News Agent", state, "Completed", start_time)
    except Exception as e:
        logger.error(f"News Agent error: {e}")
        merged_news = [{"headline": "Official emergency advisory watch active", "source": "Civil Defense", "summary": "Monitor local radio channels for updates."}]
        mon = log_node_telemetry("News Agent", state, "Failed", start_time, str(e))
        
    return {
        "news_data": merged_news,
        "monitoring_data": mon
    }

def resource_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Resource Agent.
    Locates nearby shelters, clinics, and fire stations using OSM Nominatim.
    """
    start_time = time.time()
    logger.info("Executing Resource Agent...")
    location = state.get("location") or "General Region"
    
    try:
        from tools.resource_tool import ResourceTool
        rt = ResourceTool()
        shelters = rt.find_shelters(location)
        hospitals = rt.find_hospitals(location)
        services = rt.find_emergency_services(location)
        
        resource_data = {
            "shelters": shelters,
            "hospitals": hospitals,
            "emergency_services": services,
            "source": "OpenStreetMap Nominatim"
        }
        mon = log_node_telemetry("Resource Agent", state, "Completed", start_time)
    except Exception as e:
        logger.error(f"Resource Agent node error: {e}")
        resource_data = {
            "shelters": [], "hospitals": [], "emergency_services": [],
            "source": "Fallback Cache"
        }
        mon = log_node_telemetry("Resource Agent", state, "Failed", start_time, str(e))
        
    return {
        "resource_data": resource_data,
        "monitoring_data": mon
    }

def risk_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Risk Agent.
    Computes a Gemini-powered risk index based on weather, location, and resources.
    """
    start_time = time.time()
    logger.info("Executing Risk Assessment Agent...")
    
    disaster_type = state.get("crisis_type") or "general"
    location = state.get("location") or "General Region"
    weather = state.get("weather_data") or {}
    news = state.get("news_data") or []
    resources = state.get("resource_data") or {}

    rule_score, rule_level, rule_reason = _compute_risk_assessment(disaster_type, weather, news)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=api_key)
            prompt = (
                f"You are the CrisisGuardian AI Risk Analyst. Analyze the threat profile with inputs:\n"
                f"- Disaster Type: {disaster_type}\n"
                f"- Location: {location}\n"
                f"- Weather details: {weather}\n"
                f"- News bulletins: {news}\n"
                f"- Available local facilities: {resources}\n\n"
                "Scoring rules:\n"
                "- Use Critical (9-10) ONLY for imminent life-threatening conditions matching the disaster type.\n"
                "- Use Low/Moderate (1-5) for general preparedness questions with no active emergency.\n"
                "- Do NOT escalate to Critical for unrelated weather or location alone.\n"
                "- Match severity to the stated disaster type, not worst-case assumptions.\n\n"
                "Determine:\n"
                "1. Risk Score: integer 1 to 10\n"
                "2. Risk Level: Low, Moderate, High, or Critical\n"
                "3. Risk Reason: Detailed safety evaluation justification\n\n"
                "Return ONLY a valid JSON object matching the schema:\n"
                "{\n"
                "  \"risk_score\": 7,\n"
                "  \"risk_level\": \"High\",\n"
                "  \"risk_reason\": \"Explanation details...\"\n"
                "}\n"
                "Do not include any markdown tags or comments."
            )
            response = llm.invoke(prompt)
            clean_res = response.content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_res)
            
            llm_score = int(data.get("risk_score", rule_score))
            llm_level = str(data.get("risk_level", rule_level)).title()
            llm_reason = data.get("risk_reason", rule_reason)

            # For general inquiries, cap LLM escalation to rule-based ceiling
            if disaster_type == "general":
                llm_score = min(llm_score, rule_score + 1, 5)
                llm_level = _score_to_risk_level(llm_score)
            # Prefer the more conservative (lower) score when LLM overshoots rules by 2+
            elif llm_score > rule_score + 2:
                llm_score = rule_score + 1
                llm_level = _score_to_risk_level(llm_score)
                llm_reason = f"{llm_reason} (Calibrated against operational rules: {rule_reason})"

            mon = log_node_telemetry("Risk Agent", state, "Completed", start_time)
            
            return {
                "risk_level": llm_level,
                "risk_score": llm_score,
                "risk_reason": llm_reason,
                "monitoring_data": mon
            }
        except Exception as e:
            logger.error(f"Risk Analyst LLM call failed: {e}")
            
    mon = log_node_telemetry("Risk Agent", state, "Completed", start_time)
    
    return {
        "risk_level": rule_level,
        "risk_score": rule_score,
        "risk_reason": rule_reason,
        "monitoring_data": mon
    }

def response_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Response Agent.
    Formulates a consolidated action guidelines report using Gemini.
    """
    start_time = time.time()
    logger.info("Executing Response Agent...")
    
    location = state.get("location") or "General Region"
    disaster_type = state.get("crisis_type") or "general"
    weather = state.get("weather_data") or {}
    resources = state.get("resource_data") or {}
    risk_data = {
        "risk_level": state.get("risk_level", "Moderate"),
        "risk_score": state.get("risk_score", 5),
        "risk_reason": state.get("risk_reason", "")
    }
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, google_api_key=api_key)
            prompt = (
                f"You are the CrisisGuardian AI Emergency Responder. Synthesize a life-saving safety directive for the user.\n"
                f"Location: {location}\n"
                f"Disaster Type: {disaster_type}\n"
                f"Weather Info: {weather}\n"
                f"Facilities Nearby: {resources}\n"
                f"Threat Assessment: {risk_data}\n\n"
                "Provide a clear, authoritative markdown guide containing:\n"
                "1. Immediate Actions (evacuation paths, utility alerts, life-safety rules)\n"
                "2. Specific Shelter options with names, distances, and addresses from the Facilities list\n"
                "3. Crucial contact numbers\n"
                "Keep it concise, formatting main headings in uppercase with emojis, and speak with calm authority."
            )
            response = llm.invoke(prompt)
            mon = log_node_telemetry("Response Agent", state, "Completed", start_time)
            return {
                "final_guidance": response.content,
                "monitoring_data": mon
            }
        except Exception as e:
            logger.error(f"Response Agent LLM call failed: {e}")
            
    # Mock fallback safety directive
    shelters = resources.get("shelters", [])
    shelter_str = ""
    if shelters:
        shelter_str = f"Head to the nearest shelter: **{shelters[0]['name']}** ({shelters[0]['distance_miles']} miles away, located at {shelters[0]['address']})."
    else:
        shelter_str = "Look out for municipal evacuation shelter signs."
        
    final_guidance = (
        f"🛡️ **CRITICAL EMERGENCY DIRECTIVE FOR {location.upper()}**\n\n"
        f"**Risk Severity:** {risk_data['risk_level']} (Threat Score: {risk_data['risk_score']}/10)\n"
        f"**Assessment Detail:** {risk_data['risk_reason']}\n\n"
        f"**IMMEDIATE PRECAUTIONS & PROTOCOLS:**\n"
        f"1. **Isolate Hazards**: Immediately turn off the main circuit breaker and gas valve to prevent secondary fires.\n"
        f"2. **Evacuation Action**: {shelter_str}\n"
        f"3. **Secure Supplies**: Keep a portable flashlight, mobile power banks, and essential personal papers in a waterproof container.\n"
        f"4. **Information Hub**: Stay tuned to official weather channels and avoid walking through pooled storm pools.\n\n"
        f"🚨 **RESCUE COMMAND LINE:** Reach the local Emergency dispatcher via **112** (or Police: **100**)."
    )
    
    mon = log_node_telemetry("Response Agent", state, "Completed", start_time)
    
    return {
        "final_guidance": final_guidance,
        "monitoring_data": mon
    }

def checklist_node(state: CrisisWorkflowState) -> Dict[str, Any]:
    """
    Node for the Emergency Checklist Generator.
    Creates a checklist based on the disaster type.
    """
    start_time = time.time()
    logger.info("Executing Emergency Checklist Generator...")
    
    crisis_type = state.get("crisis_type") or "general"
    crisis_type_lower = crisis_type.lower()
    
    if "flood" in crisis_type_lower:
        checklist = ["Water", "First Aid Kit", "Power Bank", "Flashlight", "Waterproof Documents"]
    elif "cyclone" in crisis_type_lower or "storm" in crisis_type_lower:
        checklist = ["Food Supplies", "Emergency Radio", "Medicines", "Batteries", "Important Documents"]
    elif "earthquake" in crisis_type_lower:
        checklist = ["Emergency Kit", "Water", "Torch", "Shoes Near Bed", "Emergency Contacts"]
    elif "fire" in crisis_type_lower:
        checklist = ["Evacuation Plan", "Fire Extinguisher", "Emergency Contacts", "Flashlight", "First Aid Kit"]
    else:
        checklist = ["Emergency Kit", "Portable Radio", "First Aid Kit", "Sanitized Water", "Warm Clothing"]
        
    mon = log_node_telemetry("Checklist Generator", state, "Completed", start_time)
    
    return {
        "checklist": checklist,
        "monitoring_data": mon
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
    builder.add_node("checklist", checklist_node)
    
    # Add sequential edges
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "weather")
    builder.add_edge("weather", "news")
    builder.add_edge("news", "resource")
    builder.add_edge("resource", "risk")
    builder.add_edge("risk", "response")
    builder.add_edge("response", "checklist")
    builder.add_edge("checklist", END)
    
    # Compile graph ready for invoke
    return builder.compile()

# Instantiated workflow for direct usage
crisis_workflow = create_crisis_workflow()

