import os
import sys

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent

# Import other agents
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent.subagents.confluence_agent import ConfluenceAgent
from agent.subagents.jira_agent import JiraAgent
from agent.subagents.llm_servier_agent import LlmServierAgent
from agent.subagents.prompt_router_agent import PromptRouterAgent
from agent.subagents.prose_agent import ProseAgent

# Configurer le projet Google Cloud (nécessaire pour ADK)
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")


class RootAgent:
    """Router agent that coordinates all specialist agents."""

    def __init__(self):
        # Initialize all sub-agents
        self.prompt_router_agent = PromptRouterAgent()
        self.confluence_agent = ConfluenceAgent()
        self.jira_agent = JiraAgent()
        self.llm_servier_agent = LlmServierAgent()
        self.prose_agent = ProseAgent()

        # Create the router agent
        self.agent = self._create_agent()

    def _create_agent(self) -> SequentialAgent:
        return SequentialAgent(
            name="root_agent",
            sub_agents=[
                self.prompt_router_agent.get_agent(),
                self.confluence_agent.get_agent(),
                self.prose_agent.get_agent(),
                self.llm_servier_agent.get_agent(),
                self.jira_agent.get_agent(),
            ],
        )


# Expose root_agent pour ADK
root_agent = RootAgent().agent
