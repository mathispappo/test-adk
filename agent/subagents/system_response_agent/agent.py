import os
import sys

from google.adk.agents import LlmAgent

# Add parent directory to path to import existing assistants
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


class SystemResponseAgent:
    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        return LlmAgent(
            name="System_Response_Regrouper",
            model="gemini-2.0-flash",
            instruction="""You are a System Response Regrouper.

            Your task is to create a full response by combining the outputs of various assistant agents.
            - confluence_agent: {confluence_output}
            - jira_agent: {jira_output}
            - prose_agent: {prose_output}
            - llm_servier_agent: {llm_servier_output}

            Use the information provided by these agents to create a coherent and comprehensive response.
            Ensure that the final response is well-structured and addresses all relevant points raised by the sub-agents.
            - Ensure that the response is clear.
            - Use the outputs from the sub-agents to form a complete and cohesive response.
            - Explain what each sub-agent contributed to the final response.
            - If any agent's output is missing, don't include it in the final response.
            """,
            description="Creates a full response with the help of all the assistant agents.",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
