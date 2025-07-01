import os
from google.adk.agents import LlmAgent
from vertexai.preview.reasoning_engines import AdkApp
from dotenv import load_dotenv
import vertexai

# Import de votre modèle custom
from .cloud_run_model import CloudRunModel

# Charger les variables d'environnement
load_dotenv()

# Configurer le projet Google Cloud (nécessaire pour ADK)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "prose-plat-sdx-275d")
vertexai.init(project=PROJECT_ID)

# Créer l'instance du modèle Cloud Run
cloud_run_model = CloudRunModel()

# Créer l'agent avec votre modèle
root_agent = LlmAgent(
    model=cloud_run_model,
    name="servier_agentic_router",
    instruction="""You are a specialized assistant trained on specific data.""",
)

# Créer l'application ADK avec le projet configuré
app = AdkApp(agent=root_agent)
