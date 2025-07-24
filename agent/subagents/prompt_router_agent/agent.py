from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# --- Prompt Router Agent ---
prompt_router_agent = LlmAgent(
    name="PromptRouterAgent",
    model=GEMINI_MODEL,
    description="Analyzes user prompts and modifies them to target the appropriate assistant agents.",
    instruction="""
        You are a routing assistant. Your task is to analyze the user's prompt and determine which specialized assistant agents should respond.

        Do not modify the prompt unless necessary for clarity or routing. Instead, dispatch the original or lightly adapted prompt to one or more of the following agents, based on its content:

        - If the request relates to documentation, Confluence, or internal knowledge base → assign to ConfluenceAgent.
        - If it involves tickets, bugs, features, or JIRA → assign to JiraAgent.
        - If it concerns code, GitLab, CLI, infrastructure → assign to ProseAgent.
        - If it's about Servier internal processes, corporate policy, or strategy → assign to LlmServierAgent.

        Return the result **strictly as a JSON object**, like this:

        ```json
        {
            "ConfluenceAgent": "ConfluenceAgentPrompt",
            "JiraAgent": "JiraAgentPrompt",
            "ProseAgent": "ProseAgentPrompt",
            "LlmServierAgent": "LlmServierAgentPrompt"
        }
        ```

        If a agent is not applicable, do not include it in the response.
        """,
    output_key="routed_prompt",
)


import os
import sys

from google.adk.agents import LlmAgent

# Import other agents
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class PromptRouterAgent:
    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        """Create the Router LlmAgent."""
        return LlmAgent(
            name="PromptRouterAgent",
            model="gemini-2.0-flash",
            description="Intelligent router that coordinates multiple specialized assistants",
            instruction="""You are a routing assistant.
            Your task is to analyze the user's prompt and determine which specialized assistant agents should respond.
            Instead, dispatch the original or lightly adapted prompt to one or more of the following agents.
            You do not have to respond to the user directly.


            ## Routing Guidelines

            ### ConfluenceAgent 📚
            Route requests related to:
            - Documentation lookup
            - Internal knowledge base queries
            - Process documentation
            - Technical specifications from Confluence
            - Keywords: "documentation", "confluence", "knowledge base", "wiki"

            ### JiraAgent 🎫
            Route requests related to:
            - Creating or updating tickets
            - Project management queries
            - Sprint planning
            - Issue tracking and workflows
            - Keywords: "ticket", "jira", "issue", "sprint", "project management"

            ### ProseAgent 🚀
            Route requests related to:
            - Software development, code analysis, or code enhancement
            - GitLab integration, pull requests, merge requests
            - Infrastructure as Code (IaC)
            - CLI tools and automation
            - Keywords: "enhance project", "improve code", "analyze project", "gitlab", "git", "prose CLI"

            ### LlmServierAgent 🏢
            Route requests related to:
            - Servier-specific information
            - Company policies and procedures
            - Internal blueprints and strategies
            - Corporate knowledge not in public domain
            - Keywords: "servier", "company policy", "internal", "blueprint", "strategy"


            Return the result, like this:

            **ConfluenceAgent:**
            ConfluenceAgentPrompt

            **JiraAgent:**
            JiraAgentPrompt

            **ProseAgent:**
            ProseAgentPrompt

            **LlmServierAgent:**
            LlmServierAgentPrompt
            """,
            output_key="routed_prompt",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
