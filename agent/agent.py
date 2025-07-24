import os

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent

from .subagents.confluence_agent import confluence_agent
from .subagents.jira_agent import jira_agent
from .subagents.llm_servier_agent import llm_servier_agent
from .subagents.prompt_router_agent import prompt_router_agent
from .subagents.prose_agent import prose_agent
from .subagents.system_response_regrouper import system_response_regrouper

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")


# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="System_Response_Regrouper_Root_Agent",
    sub_agents=[
        prompt_router_agent,
        confluence_agent,
        jira_agent,
        prose_agent,
        llm_servier_agent,
        system_response_regrouper,
    ],
)


import os
import sys

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent

# Import other agents
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent.subagents.manager_agent import ManagerAgent
from agent.subagents.prompt_router_agent import PromptRouterAgent

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
        self.manager_agent = ManagerAgent()

        # Create the router agent
        self.agent = self._create_agent()

    def _create_agent(self) -> SequentialAgent:
        return SequentialAgent(
            name="root_agent",
            sub_agents=[
                self.prompt_router_agent.get_agent(),
                self.manager_agent.get_agent(),
            ],
        )


# Expose root_agent pour ADK
root_agent = RootAgent().agent
