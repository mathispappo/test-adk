from google.adk.agents import LlmAgent
# import os
# from dotenv import load_dotenv
# import vertexai

# Import de votre modèle custom
from .cloud_run_model import CloudRunModel

# Charger les variables d'environnement
# load_dotenv()

# # Configurer le projet Google Cloud (nécessaire pour ADK)
# PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "prose-plat-sdx-275d")
# vertexai.init(project=PROJECT_ID)

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

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
