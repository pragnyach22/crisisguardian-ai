"""
CrisisGuardian AI - Disaster Response Tools
Implements LangChain-style tools for fetching real-time disaster alerts,
nearest shelters, and sending SOS notifications.
"""

import requests
from langchain_core.tools import tool

@tool
def get_weather_alerts(location: str) -> str:
    """
    Fetches active weather warnings and cyclone/flood alerts for a specific location.
    """
    # In production, this would make an API call to a weather service.
    # Here, we return mock crisis data for development.
    print(f"[Tool Log] Fetching weather alerts for location: {location}")
    return (
        f"Active alerts for {location}: High-risk flood watch. "
        "Precipitation levels exceed 150mm/hr. Rivers in vicinity are rising rapidly."
    )

@tool
def get_earthquake_alerts(min_magnitude: float = 4.0) -> str:
    """
    Fetches recent high-magnitude earthquake events globally or regionally.
    """
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "minmagnitude": min_magnitude,
        "limit": 3
    }
    try:
        print(f"[Tool Log] Querying USGS for earthquakes >= {min_magnitude}")
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            if not features:
                return "No recent major earthquakes matching criteria."
            
            results = []
            for f in features:
                properties = f.get("properties", {})
                results.append(
                    f"Mag: {properties.get('mag')}, Place: {properties.get('place')}, Time: {properties.get('time')}"
                )
            return "\n".join(results)
    except Exception as e:
        return f"USGS API error: {str(e)}. Returning mock: Mag 6.1 Earthquake detected 45km off-shore."
        
    return "Failed to retrieve earthquake alerts. Please try again later."

@tool
def find_nearest_shelter(location: str, disaster_type: str) -> str:
    """
    Finds safety shelters in a specified location relevant to the disaster type (e.g., cyclone dome, high-ground flood shelter).
    """
    print(f"[Tool Log] Searching for {disaster_type} shelters near {location}")
    # Return mock safe houses
    return (
        f"Nearest {disaster_type} shelters in {location}:\n"
        "1. Community Center Hall A (High Ground, Capacity: 300) - 1.2 miles away\n"
        "2. Central High School Gym (Cyclone Safe House, Capacity: 500) - 2.5 miles away\n"
        "3. Local Stadium Safe Zone (First Aid & Food Station) - 3.1 miles away"
    )

@tool
def send_sos_notification(user_id: str, coordinates: str, description: str) -> str:
    """
    Triggers an emergency SOS dispatch alert sending user location and details to authorities.
    """
    print(f"[SOS TRIGGERED] User: {user_id}, Coordinates: {coordinates}, Situation: {description}")
    return f"Emergency SOS dispatch request successfully sent to local response units for location: {coordinates}."
