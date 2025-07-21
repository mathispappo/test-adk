import os

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent

from .subagents.manager_agent import manager_agent
from .subagents.prompt_router_agent import prompt_router_agent
from .subagents.system_response_regrouper import system_response_regrouper

# Configurer le projet Google Cloud (nécessaire pour ADK)
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")


# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[
        prompt_router_agent,
        manager_agent,
        system_response_regrouper,
    ],  # Ensure system_response_regrouper is included
)
