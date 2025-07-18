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
        """,
    output_key="prose_output",
)
