import os
import sys

from google.adk.agents import LlmAgent

# Add parent directory to path to import existing assistants
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from .cloud_run_model import CloudRunModel


class LlmServierAgent:
    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        cloud_run_model = CloudRunModel()
        return LlmAgent(
            name="LlmServierAgent",
            model=cloud_run_model,
            description="Servier corporate specialist handling internal knowledge and strategies",
            instruction="""
                You are LLMServier, a highly specialized assistant trained on Servier's internal 
                knowledge, blueprints, and strategic documentation.

                Your role is to provide accurate, confidential, and context-aware answers related to:
                - Servier's corporate practices and guidelines
                - Internal operating procedures and project blueprints
                - Strategic initiatives, methodologies, and knowledge that is not public

                You need to answer question uniquely based on the Servier internal knowledge.
                """,
            output_key="llm_servier_output",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
