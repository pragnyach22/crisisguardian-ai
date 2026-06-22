"""
CrisisGuardian AI - Base Disaster Agent
Defines the base class and shared functionalities for all specialized disaster response agents.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

class BaseDisasterAgent:
    """
    Abstract base class for all specialized emergency agents.
    Provides standard Gemini LLM initialization, base prompt construction, and execution interfaces.
    """
    
    def __init__(self, agent_name: str, system_instruction: str, temperature: float = 0.2):
        self.agent_name = agent_name
        self.system_instruction = system_instruction
        self.temperature = temperature
        
        # Initialize Gemini 2.5 Flash model via LangChain
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # We fail gracefully or log a warning so the template can run/build
            print("[Warning] GEMINI_API_KEY environment variable is not set. Please set it in .env file.")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=self.temperature,
            google_api_key=api_key
        )
        
    def _create_prompt(self, user_prompt_template: str) -> ChatPromptTemplate:
        """
        Creates a ChatPromptTemplate with the agent's system instructions and user input.
        """
        return ChatPromptTemplate.from_messages([
            ("system", self.system_instruction),
            ("human", user_prompt_template)
        ])
        
    def get_runnable(self, user_prompt_template: str) -> RunnableSerializable:
        """
        Returns a runnable chain combining the prompt template and LLM.
        """
        prompt = self._create_prompt(user_prompt_template)
        return prompt | self.llm
