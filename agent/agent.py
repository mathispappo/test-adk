from google.adk.agents import LlmAgent
from vertexai.preview.reasoning_engines import AdkApp
from dotenv import load_dotenv

# Import de votre modèle custom
from .cloud_run_model import CloudRunModel

# Charger les variables d'environnement
load_dotenv()

# S'assurer que l'authentification Google est configurée
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS",
#     os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
# )

# Créer l'instance du modèle Cloud Run
cloud_run_model = CloudRunModel()

# Créer l'agent avec votre modèle
root_agent = LlmAgent(
    model=cloud_run_model,
    name="servier_agentic_router",
    instruction="You are a specialized assistant trained on specific data.",
)
# Créer l'application ADK
app = AdkApp(agent=root_agent)
