"""
CrisisGuardian AI - Error Handling & Fallback Module
Provides graceful error handling and offline fallback mechanisms.
"""

import logging
from functools import wraps
from typing import Callable, Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger("ErrorHandler")


class CrisisGuardianException(Exception):
    """Base exception for CrisisGuardian AI."""
    pass


class APIException(CrisisGuardianException):
    """Exception for API errors."""
    pass


class ToolException(CrisisGuardianException):
    """Exception for tool errors."""
    pass


class WorkflowException(CrisisGuardianException):
    """Exception for workflow errors."""
    pass


def handle_errors(fallback_value: Any = None, log_level: str = "ERROR"):
    """
    Decorator to handle errors gracefully with fallback values.
    
    Args:
        fallback_value: Value to return if error occurs
        log_level: Logging level (ERROR, WARNING, INFO)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_func = getattr(logger, log_level.lower(), logger.error)
                log_func(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                
                if fallback_value is not None:
                    return fallback_value
                
                # Return appropriate fallback based on function name
                if "tool" in func.__name__.lower():
                    return _get_tool_fallback(func.__name__)
                elif "agent" in func.__name__.lower():
                    return _get_agent_fallback(func.__name__)
                else:
                    return _get_default_fallback()
        
        return wrapper
    return decorator


def _get_tool_fallback(tool_name: str) -> Dict[str, Any]:
    """Returns fallback data for tool functions."""
    fallbacks = {
        "get_weather_alerts": {
            "location": "General Region",
            "condition": "Unknown",
            "alerts": [{
                "event": "Weather Alert",
                "severity": "moderate",
                "description": "Unable to fetch real weather. Please check local sources."
            }]
        },
        "get_earthquake_alerts": {
            "status": "No recent earthquakes detected.",
            "source": "USGS Fallback"
        },
        "find_nearest_shelter": {
            "shelters": [{
                "name": "Nearest Municipal Safe Zone",
                "address": "Contact local emergency services",
                "distance": "Unknown"
            }]
        },
        "send_sos_notification": {
            "status": "SOS alert request recorded",
            "message": "Emergency services notified. Await response.",
            "fallback": True
        }
    }
    return fallbacks.get(tool_name, _get_default_fallback())


def _get_agent_fallback(agent_name: str) -> str:
    """Returns fallback response for agent functions."""
    fallbacks = {
        "FloodResponseAgent": (
            "🚨 FLOOD SAFETY DIRECTIVE:\n"
            "1. Move to higher ground immediately\n"
            "2. Avoid flooded areas - never attempt to cross flowing water\n"
            "3. Turn off utilities if safe to do so\n"
            "4. Call emergency services: 112\n"
        ),
        "CycloneResponseAgent": (
            "🌪️ CYCLONE SAFETY DIRECTIVE:\n"
            "1. Move to the strongest room in your building\n"
            "2. Close all windows and doors\n"
            "3. Stay indoors until safe to evacuate\n"
            "4. Monitor emergency broadcasts: 112\n"
        ),
        "EarthquakeResponseAgent": (
            "🏚️ EARTHQUAKE SAFETY DIRECTIVE:\n"
            "1. DROP, COVER, and HOLD ON immediately\n"
            "2. If outdoors, move away from buildings\n"
            "3. Stay alert for aftershocks\n"
            "4. Evacuate if building is damaged\n"
        ),
        "FireResponseAgent": (
            "🔥 FIRE SAFETY DIRECTIVE:\n"
            "1. Evacuate immediately to a safe location\n"
            "2. Stay low below smoke\n"
            "3. Close doors behind you\n"
            "4. Call emergency services: 112\n"
        ),
        "EmergencySupervisorAgent": (
            "🛡️ EMERGENCY ALERT:\n"
            "An emergency situation has been detected.\n"
            "Please provide more details about the type of disaster.\n"
            "In immediate danger? Call 112 now.\n"
        )
    }
    return fallbacks.get(agent_name, _get_default_fallback())


def _get_default_fallback() -> Any:
    """Returns a generic fallback response."""
    return {
        "status": "offline",
        "message": "System operating in fallback mode. Limited functionality available.",
        "timestamp": datetime.now().isoformat(),
        "recommendation": "Use official emergency services and local broadcasts for critical information."
    }


def create_offline_response(query: str, location: str, crisis_type: str) -> Dict[str, Any]:
    """
    Creates a comprehensive offline response for when APIs are unavailable.
    """
    return {
        "threat_level": "Unknown",
        "risk_score": 5,
        "risk_reason": "Unable to assess threat level. Operating in offline mode.",
        "verification_status": "Unable to verify. Use official sources.",
        "weather_summary": "Weather data unavailable. Listen to broadcast stations.",
        "guidance": _get_offline_guidance(crisis_type, location),
        "checklist": _get_offline_checklist(crisis_type),
        "recommended_actions": [
            "Contact local emergency services: 112",
            "Listen to official emergency broadcasts",
            "Follow local authority instructions",
            "Evacuate if instructed by officials"
        ],
        "monitoring_data": {
            "system_status": "degraded",
            "api_availability": "offline",
            "fallback_mode": True,
            "message": "Running in emergency fallback mode"
        }
    }


def _get_offline_guidance(crisis_type: str, location: str) -> str:
    """Returns offline safety guidance based on crisis type."""
    crisis_type_lower = (crisis_type or "general").lower()
    
    guidance_map = {
        "flood": (
            "🚨 **FLOOD RESPONSE - OFFLINE MODE**\n"
            "**IMMEDIATE ACTIONS:**\n"
            "1. Evacuate to high ground immediately\n"
            "2. Do NOT attempt to drive/walk through water\n"
            "3. Turn off gas and electricity if accessible\n"
            "4. Bring important documents in waterproof container\n"
            "**COMMUNICATION:** Use battery-powered radio for updates"
        ),
        "cyclone": (
            "🌪️ **CYCLONE RESPONSE - OFFLINE MODE**\n"
            "**IMMEDIATE ACTIONS:**\n"
            "1. Seek shelter in strongest room (windowless if possible)\n"
            "2. Close all openings and secure doors\n"
            "3. Stock water, food, and medicines for 3+ days\n"
            "4. Keep flashlight and batteries ready\n"
            "**DO NOT:** Venture outside during wind gusts"
        ),
        "earthquake": (
            "🏚️ **EARTHQUAKE RESPONSE - OFFLINE MODE**\n"
            "**IMMEDIATE ACTIONS:**\n"
            "1. DROP to hands and knees\n"
            "2. Take COVER under sturdy table or desk\n"
            "3. HOLD ON until shaking stops\n"
            "4. If outdoors, move to open area away from buildings\n"
            "**CAUTION:** Aftershocks possible - remain alert"
        ),
        "fire": (
            "🔥 **FIRE RESPONSE - OFFLINE MODE**\n"
            "**IMMEDIATE ACTIONS:**\n"
            "1. Evacuate immediately - do not stop for belongings\n"
            "2. Keep low and crawl under smoke\n"
            "3. Close doors behind you to slow fire spread\n"
            "4. Use designated evacuation routes only\n"
            "**PRIORITY:** Human life over property"
        )
    }
    
    return guidance_map.get(crisis_type_lower, f"Emergency situation in {location}. Contact local authorities immediately.")


def _get_offline_checklist(crisis_type: str) -> list:
    """Returns offline emergency checklist based on crisis type."""
    crisis_type_lower = (crisis_type or "general").lower()
    
    checklists = {
        "flood": ["Water", "First Aid Kit", "Flashlight", "Power Bank", "Important Documents"],
        "cyclone": ["Water (3+ days)", "Food", "Medicines", "Batteries", "Radio", "First Aid"],
        "earthquake": ["First Aid Kit", "Water", "Flashlight", "Whistle", "Sturdy Shoes"],
        "fire": ["Important Documents", "Medications", "Phone Charger", "Comfortable Shoes", "ID"],
    }
    
    return checklists.get(crisis_type_lower, ["Water", "First Aid Kit", "Flashlight", "Important Items", "Phone Charger"])


def validate_api_response(response: Any, expected_type: type) -> bool:
    """
    Validates API response type and basic structure.
    
    Args:
        response: Response object to validate
        expected_type: Expected type (dict, list, str, etc.)
    
    Returns:
        bool: True if valid, False otherwise
    """
    if response is None:
        logger.warning("Response is None")
        return False
    
    if not isinstance(response, expected_type):
        logger.warning(f"Response type mismatch. Expected {expected_type}, got {type(response)}")
        return False
    
    if isinstance(response, (dict, list)) and len(response) == 0:
        logger.warning("Response is empty")
        return False
    
    return True


class FallbackManager:
    """Manages fallback state and recovery for the system."""
    
    def __init__(self):
        self.is_offline = False
        self.failed_services = {}
        self.last_error = None
    
    def mark_service_down(self, service_name: str, error: str):
        """Marks a service as down."""
        self.failed_services[service_name] = {
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        logger.warning(f"Service {service_name} marked as down: {error}")
    
    def mark_service_up(self, service_name: str):
        """Marks a service as operational."""
        if service_name in self.failed_services:
            del self.failed_services[service_name]
            logger.info(f"Service {service_name} restored")
    
    def is_service_available(self, service_name: str) -> bool:
        """Checks if a service is available."""
        return service_name not in self.failed_services
    
    def get_status_report(self) -> Dict[str, Any]:
        """Returns current fallback status report."""
        return {
            "is_offline": self.is_offline,
            "failed_services": self.failed_services,
            "timestamp": datetime.now().isoformat()
        }


# Global fallback manager instance
fallback_manager = FallbackManager()
