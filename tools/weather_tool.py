"""
CrisisGuardian AI - Weather Tool
================================
Provides real-time weather data and alert integration.
Supports OpenWeatherMap API with graceful fallback to mock data.
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("WeatherTool")

class WeatherTool:
    """
    Object-oriented handler for obtaining real-time meteorological data,
    cyclone warnings, and flood precipitation metrics.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the weather tool with optional API authentication.

        Args:
            api_key (str, optional): Key for weather services (e.g. OpenWeatherMap).
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.timeout = 5

    def get_current_weather(self, location: str, crisis_type: str = "general") -> Dict[str, Any]:
        """
        Retrieves the current weather state for a specified city or coordinates.
        Falls back to mock data if API is unavailable.

        Args:
            location (str): Name of the city or coordinates (e.g. 'Miami, FL').
            crisis_type (str): Active disaster context to tune mock fallbacks.

        Returns:
            Dict[str, Any]: Consolidated weather measurements (temperature, wind, etc.).
        """
        api_key = self.api_key or os.getenv("OPENWEATHER_API_KEY")
        if not api_key or api_key == "your_openweather_api_key_here":
            return self._get_mock_weather(location, crisis_type)
            
        try:
            logger.info(f"Fetching real weather for {location}")
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                main = data.get("main", {})
                wind = data.get("wind", {})
                weather = data.get("weather", [{}])[0]
                return {
                    "location": location,
                    "temperature_c": main.get("temp", 25.0),
                    "humidity": main.get("humidity", 60),
                    "wind_speed_kmh": round(wind.get("speed", 0.0) * 3.6, 2), # convert m/s to km/h
                    "condition": weather.get("main", "Clear"),
                    "description": weather.get("description", "clear sky"),
                    "source": "OpenWeatherMap API"
                }
        except Exception:
            pass
            
        return self._get_mock_weather(location, crisis_type)

    def _get_mock_weather(self, location: str, crisis_type: str = "general") -> Dict[str, Any]:
        """
        Generates structured mock weather statistics based on crisis type and location.
        Mock data is scoped to the active disaster context so unrelated queries
        are not always escalated to cyclone-level conditions.
        """
        crisis_type = (crisis_type or "general").lower()
        location_lower = (location or "").lower()

        if crisis_type == "cyclone":
            return {
                "location": location,
                "temperature_c": 29.0,
                "humidity": 90,
                "wind_speed_kmh": 78.0,
                "condition": "Cyclone",
                "description": "cyclonic storm winds",
                "source": "Mock Fallback Feed"
            }
        if crisis_type == "flood":
            return {
                "location": location,
                "temperature_c": 28.5,
                "humidity": 85,
                "wind_speed_kmh": 35.0,
                "condition": "Heavy Rain",
                "description": "severe monsoon downpour",
                "source": "Mock Fallback Feed"
            }
        if crisis_type == "fire":
            return {
                "location": location,
                "temperature_c": 38.0,
                "humidity": 20,
                "wind_speed_kmh": 25.0,
                "condition": "Clear",
                "description": "dry and windy conditions",
                "source": "Mock Fallback Feed"
            }
        if crisis_type == "earthquake":
            return {
                "location": location,
                "temperature_c": 24.0,
                "humidity": 50,
                "wind_speed_kmh": 10.0,
                "condition": "Clear",
                "description": "calm conditions — seismic activity not visible in weather data",
                "source": "Mock Fallback Feed"
            }

        # General / preparedness inquiries — neutral baseline regardless of location
        return {
            "location": location,
            "temperature_c": 24.5,
            "humidity": 55,
            "wind_speed_kmh": 12.0,
            "condition": "Cloudy",
            "description": "scattered clouds, no active severe weather",
            "source": "Mock Fallback Feed"
        }

    def get_weather_alerts(self, location: str, crisis_type: str = "general") -> List[Dict[str, Any]]:
        """
        Retrieves active weather bulletins or flood warnings for the specified region.

        Args:
            location (str): Geographical area description.
            crisis_type (str): Active disaster context to scope alert severity.

        Returns:
            List[Dict[str, Any]]: List of active alert alerts.
        """
        crisis_type = (crisis_type or "general").lower()
        weather = self.get_current_weather(location, crisis_type)
        cond = weather.get("condition", "").lower()
        wind = weather.get("wind_speed_kmh", 0.0)
        
        alerts = []
        if crisis_type == "flood" and ("rain" in cond or "drizzle" in cond or "thunderstorm" in cond):
            alerts.append({
                "event": "Flash Flood Watch",
                "severity": "Severe",
                "description": f"Heavy rain detected ({weather.get('description', '')}). Drainage systems may experience sudden surge rises.",
                "ends_at": "Next 24 hours"
            })
        if crisis_type == "cyclone" and (wind > 50 or "cyclone" in cond or "storm" in cond):
            alerts.append({
                "event": "High Wind Warning",
                "severity": "Extreme",
                "description": f"Severe wind gusts ({wind} km/h) forecasted. Structural damage and debris hazards possible.",
                "ends_at": "Next 12 hours"
            })
        if crisis_type == "fire":
            alerts.append({
                "event": "Fire Weather Watch",
                "severity": "Moderate",
                "description": "Dry and windy conditions may accelerate fire spread.",
                "ends_at": "Next 24 hours"
            })

        return alerts

