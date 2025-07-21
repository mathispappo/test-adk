from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from .subagents.confluence_agent import confluence_agent
from .subagents.jira_agent import jira_agent
from .subagents.llm_servier_agent import llm_servier_agent
from .subagents.prose_agent import prose_agent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Confluence Agent
confluence_agent = LlmAgent(
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
