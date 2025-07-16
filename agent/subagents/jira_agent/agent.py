from google.adk.agents import LlmAgent


# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Jira Agent
jira_agent = LlmAgent(
    name="JiraAgent",
    model="gemini-2.0-flash",
    description="Project management specialist handling JIRA tickets and workflows",
    instruction="""
        You are a JIRA ticket assistant. Your role is to help users create and manage 
        well-structured JIRA tickets. When a user provides a request for a ticket, analyze the request 
        and propose ticket details.
        
        For development work, migrations, implementations, and new functionality, use "Feature" as the issue type.
        For defects and fixes, use "Bug" as the issue type.
        For user stories and requirements, use "Story" as the issue type.
        """,
    output_key="jira_output",
)
