import os
import sys

from google.adk.agents import LlmAgent

# Import other agents
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent.subagents.confluence_agent.agent import ConfluenceAgent
from agent.subagents.jira_agent.agent import JiraAgent
from agent.subagents.llm_servier_agent.agent import LlmServierAgent
from agent.subagents.prose_agent.agent import ProseAgent


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
            For each agent prompt block (e.g. 'ConfluenceAgent: ...', 'ProseAgent: ...'), transfer that block to the corresponding agent using the transfer_to_agent function.
            If multiple agent blocks are present, transfer each to its respective agent, one after the other, until all blocks have been transferred.
            Do not answer yourself unless you are the best agent for the prompt.
            Only transfer the relevant prompt part to the agent.
            Example:
            **ConfluenceAgent:**
            <prompt for confluence>
            **ProseAgent:**
            <prompt for prose>
            **JiraAgent:**
            <prompt for jira>
            **LlmServierAgent:**
            <prompt for servier>
            If you receive several blocks, call transfer_to_agent for each block in sequence.
            """,
            sub_agents=[
                self.prose_agent.get_agent(),
                self.confluence_agent.get_agent(),
                self.jira_agent.get_agent(),
                self.llm_servier_agent.get_agent(),
            ],
            output_key="manager_response",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
