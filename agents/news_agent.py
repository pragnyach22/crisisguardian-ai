"""
CrisisGuardian AI - News Agent
==============================
Responsibility:
- Gathers active disaster-related news, public broadcasts, and government emergency announcements.
- Monitors feeds for official evacuation zones, curfew alerts, and public safety statements.
"""

from google.adk.agents import Agent

# Initialize the Google ADK News Agent skeleton
news_agent = Agent(
    name="news_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the CrisisGuardian AI News Analyst. Your responsibilities are:\n"
        "1. Retrieve recent news feeds, civil defense bulletins, and municipal safety notices.\n"
        "2. Filter reports to identify officially verified instructions vs. unverified social media updates.\n"
        "3. Focus on road closures, bridges down, utility outages, and public transport cancellations.\n"
        "Be extremely objective and verify sources prior to confirming emergency directives."
    ),
    tools=[]  # Future tools: search_news, fetch_civil_defense_bulletins
)

# Placeholder for custom news crawling / API helper functions
def retrieve_emergency_news(location: str) -> list:
    """
    Skeleton function to retrieve news and social alerts from official channels.
    
    Args:
        location (str): The target geographic location.
        
    Returns:
        list: A list of active verified bulletins and news items.
    """
    # TODO: Implement RSS feed parser or news API search
    return []
