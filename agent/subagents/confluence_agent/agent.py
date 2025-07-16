from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Confluence Agent
confluence_agent = LlmAgent(
    name="ConfluenceAgent",
    model="gemini-2.0-flash",
    description="Documentation specialist handling Confluence knowledge base operations",
    instruction="""
        You are a Confluence knowledge assistant. 
        You help users by providing accurate information from the company's Confluence knowledge base.
        Find some information on the web and provide it to the user.
        """,
    output_key="confluence_output",
)
