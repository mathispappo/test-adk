from google.adk.agents import SequentialAgent

from .subagents.prompt_router_agent import prompt_router_agent
from .subagents.confluence_agent import confluence_agent
from .subagents.jira_agent import jira_agent
from .subagents.llm_servier_agent import llm_servier_agent
from .subagents.prose_agent import prose_agent
from .subagents.system_response_regrouper import system_response_regrouper

from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
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
