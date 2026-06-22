"""
CrisisGuardian AI Tools Package
Defines custom tools for disaster assistance: fetching weather alerts, finding nearby shelters,
triggering emergency alerts (SOS), and the object-oriented Weather, News, and Resource tools.
"""

from .disaster_tools import (
    get_weather_alerts,
    get_earthquake_alerts,
    find_nearest_shelter,
    send_sos_notification
)

from .weather_tool import WeatherTool
from .news_tool import NewsTool
from .resource_tool import ResourceTool

__all__ = [
    "get_weather_alerts",
    "get_earthquake_alerts",
    "find_nearest_shelter",
    "send_sos_notification",
    "WeatherTool",
    "NewsTool",
    "ResourceTool"
]

