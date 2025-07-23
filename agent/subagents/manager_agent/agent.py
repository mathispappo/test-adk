import os
import sys

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Import other agents
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent.subagents.confluence_agent import ConfluenceAgent
from agent.subagents.jira_agent import JiraAgent
from agent.subagents.llm_servier_agent import LlmServierAgent
from agent.subagents.prose_agent import ProseAgent


class ManagerAgent:
    """Router agent that coordinates all specialist agents."""

    def __init__(self):
        # Initialize all sub-agents
        self.confluence_agent = ConfluenceAgent()
        self.jira_agent = JiraAgent()
        self.llm_servier_agent = LlmServierAgent()
        self.prose_agent = ProseAgent()

        # Create the router agent
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create the Router LlmAgent."""
        # Manager Agent
        return LlmAgent(
            name="ManagerAgent",
            model="gemini-2.0-flash",
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
                AgentTool(self.prose_agent.get_agent()),
                AgentTool(self.confluence_agent.get_agent()),
                AgentTool(self.jira_agent.get_agent()),
                AgentTool(self.llm_servier_agent.get_agent()),
            ],
            output_key="manager_response",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
