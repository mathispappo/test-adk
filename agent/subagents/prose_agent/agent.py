from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Prose Agent
prose_agent = LlmAgent(
    name="ProseAgent",
    model="gemini-2.0-flash",
    description="Software development specialist handling code, infrastructure, GitLab integration, and CLI tasks",
    instruction="""
        You are Prose, an AI assistant that specializes in code enhancement and GitLab integration.

        You can help with:
        1. **Enhancing GitLab projects** - Provide a GitLab project URL and analyze/improve the code
        2. **Creating Pull Requests** - Automatically create MRs with enhanced code
        3. **Answering development questions** - General coding and infrastructure help
        

        You need to answer question uniquely based on the GitLab project.
        If there is nothing relevant in the GitLab project, you should not answer the question, leaving it unanswered, don't write anything.

        Here is the prompt you need to answer:
        {routed_prompt}

        If on the prompt you find "ProseAgent", you should return the output in the following JSON format:
        ```json
        {
            "prose_output": "ProseAgentResponse"
        }
        ```
        """,
    output_key="prose_output",
)


import os
import sys

from google.adk.agents import LlmAgent

# Add parent directory to path to import existing assistants
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


class ProseAgent:
    """Prose specialist agent for software development."""

    def __init__(self):
        self.agent = self._create_agent()

    def _create_agent(self) -> LlmAgent:
        return LlmAgent(
            name="ProseAgent",
            model="gemini-2.0-flash",
            description="Software development specialist handling code, infrastructure, GitLab integration, and CLI tasks",
            instruction="""
                You are Prose, an AI assistant that specializes in code enhancement and GitLab integration.

                You can help with:
                1. **Enhancing GitLab projects** - Provide a GitLab project URL and analyze/improve the code
                2. **Creating Pull Requests** - Automatically create MRs with enhanced code
                3. **Answering development questions** - General coding and infrastructure help
                """,
            output_key="prose_output",
        )

    def get_agent(self) -> LlmAgent:
        """Return the configured LlmAgent."""
        return self.agent
