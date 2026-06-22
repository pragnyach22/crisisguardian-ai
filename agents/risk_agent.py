"""
CrisisGuardian AI - Risk Agent
==============================
Responsibility:
- Gathers data from the Weather Agent, News Agent, and user's inputs.
- Synthesizes warnings, proximity to hazard vectors, and terrain vulnerability.
- Assigns a logical risk category (Low, Moderate, High, Extreme) and computes risk indexes.
"""

from google.adk.agents import Agent

# Initialize the Google ADK Risk Agent skeleton
risk_agent = Agent(
    name="risk_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the CrisisGuardian AI Risk Analyst. Your responsibilities are:\n"
        "1. Analyze combined inputs from weather forecasting, official warning reports, and user-provided descriptions.\n"
        "2. Assess immediate threats to life, property structures, and escape networks.\n"
        "3. Standardize output into risk severity categories: Low, Moderate, High, Extreme.\n"
        "Provide logical reasoning explaining why a specific level was assigned."
    ),
    tools=[]  # Future tools: run_risk_matrix_calculation
)

# Placeholder for risk analysis algorithm or matrix logic
def calculate_risk_matrix(weather_score: float, structural_hazard: float) -> str:
    """
    Skeleton function calculating composite risk severity indicators.
    
    Args:
        weather_score (float): Numeric scale representing weather threat level.
        structural_hazard (float): Numeric scale representing local structural stability/terrain risk.
        
    Returns:
        str: Computed threat level category.
    """
    # TODO: Implement mathematical risk indexing model
    return "unknown"
