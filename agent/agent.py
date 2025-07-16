import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import agent_tool

from .subagents.confluence_agent import confluence_agent
from .subagents.jira_agent import jira_agent
from .subagents.llm_servier_agent import llm_servier_agent
from .subagents.prompt_router_agent import prompt_router_agent
from .subagents.prose_agent import prose_agent
from .subagents.system_response_regrouper import system_response_regrouper

# Configurer le projet Google Cloud (nécessaire pour ADK)
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")


# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# --- Manager Agent ---
manager_agent = LlmAgent(
    name="ManagerAgent",
    model=GEMINI_MODEL,
    description="Manages the system response regrouper and routes prompts to appropriate sub-agents-tools.",
    instruction="""
    You are a Manager Agent. Your task is to manage the system response regrouper and route prompts to the appropriate sub-agents-tools.
    - If the request relates to ConfluenceAgent → assign to ConfluenceAgent.
    - If the request relates to JiraAgent → assign to JiraAgent.
    - If the request relates to ProseAgent → assign to ProseAgent.
    - If the request relates to LlmServierAgent → assign to LlmServierAgent.

    You just have to replace the XXXAgentPrompt with the actual prompt for each agent.
    Juste replace the placeholders with the actual prompts.

    {routed_prompt}
    """,
    tools=[
        agent_tool.AgentTool(agent=confluence_agent),
        agent_tool.AgentTool(agent=jira_agent),
        agent_tool.AgentTool(agent=prose_agent),
        agent_tool.AgentTool(agent=llm_servier_agent),
    ],
    output_key="manager_response",
)

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[
        prompt_router_agent,
        manager_agent,
        system_response_regrouper,
    ],  # Ensure system_response_regrouper is included
)
