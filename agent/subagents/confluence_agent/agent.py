import os
import sys

from google.adk.agents import LlmAgent

# Add parent directory to path to import existing assistants
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


class ConfluenceAgent:
    """Confluence specialist agent for documentation queries."""

    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        return LlmAgent(
            name="ConfluenceAgent",
            model="gemini-2.0-flash",
            description="Documentation specialist handling Confluence knowledge base operations",
            instruction="""
                You are a Confluence knowledge assistant. 
                You help users by providing accurate information from the company's Confluence knowledge base.
                Find some information on the web and provide it to the user.
                """,
            output_key="confluence_output",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
