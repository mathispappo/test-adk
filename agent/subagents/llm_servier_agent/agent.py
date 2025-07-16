from google.adk.agents import LlmAgent

from .cloud_run_model import CloudRunModel

# Créer l'instance du modèle Cloud Run
cloud_run_model = CloudRunModel()

# LLM Servier Agent
llm_servier_agent = LlmAgent(
    name="LlmServierAgent",
    model=cloud_run_model,
    description="Servier corporate specialist handling internal knowledge and strategies",
    instruction="""
        You are LLMServier, a highly specialized assistant trained on Servier's internal 
        knowledge, blueprints, and strategic documentation.

        Your role is to provide accurate, confidential, and context-aware answers related to:
        - Servier's corporate practices and guidelines
        - Internal operating procedures and project blueprints
        - Strategic initiatives, methodologies, and knowledge that is not public

        You need to answer question uniquely based on the Servier internal knowledge.
        """,
    output_key="llm_servier_output",
)
