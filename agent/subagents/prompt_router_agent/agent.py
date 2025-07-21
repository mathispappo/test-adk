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

            ConfluenceAgent:
            ConfluenceAgentPrompt

            JiraAgent:
            JiraAgentPrompt

            ProseAgent:
            ProseAgentPrompt

            LlmServierAgent:
            LlmServierAgentPrompt
            """,
            output_key="routed_prompt",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
