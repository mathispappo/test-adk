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
        - If it's about Servier internal processes, corporate policy, blueprint, or strategy → assign to LlmServierAgent.

        If a agent is not applicable, do not include it in the response.

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
