"""
CrisisGuardian AI - Response Agent
==================================
Responsibility:
- Compiles findings from the Coordinator, Weather, News, Resource, and Risk Agents.
- Formulates clean, step-by-step guidance checklists and safety instructions.
- Provides immediate actions for the user, emergency helpline numbers, and next steps.
"""

from google.adk.agents import Agent

# Initialize the Google ADK Response Agent skeleton
response_agent = Agent(
    name="response_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the CrisisGuardian AI Emergency Responder. Your responsibilities are:\n"
        "1. Read the combined report detailing weather threats, active news alerts, available shelters, and calculated risk level.\n"
        "2. Structure emergency guidance into highly readable, bulleted emergency lists.\n"
        "3. Emphasize physical survival rules (evacuation paths, cover rules, utility warnings) at the absolute top.\n"
        "Speak with authority, clarity, and urgent care."
    ),
    tools=[]  # Future tools: generate_emergency_pdf, send_sms_alert
)

# Placeholder for final report formatting
def generate_safety_checklist(analysis_report: dict) -> str:
    """
    Skeleton function formatting the synthesized response for final user display.
    
    Args:
        analysis_report (dict): Unified state data compiled by the coordinator.
        
    Returns:
        str: Styled Markdown guidance output.
    """
    # TODO: Implement markdown compiler for structured safety lists
    return ""
