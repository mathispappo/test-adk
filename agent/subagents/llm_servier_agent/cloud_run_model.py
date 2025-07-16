import google.auth
import google.oauth2.id_token
import google.auth.transport.requests
from google.adk.models.lite_llm import LiteLlm
import requests
import json
import litellm
from typing import Optional
from litellm import CustomLLM
import subprocess


class CloudRunCodeLlama(CustomLLM):
    """Custom LLM handler pour Cloud Run"""

    def __init__(self):
        self.service_url = "http://34.107.178.200"
        self.request = google.auth.transport.requests.Request()

    def get_identity_token(self) -> str:
        """Obtenir un token d'identité Google valide"""
        try:
            result = subprocess.run(
                ["gcloud", "auth", "print-identity-token"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'obtention du token: {e}")
            raise Exception("Impossible d'obtenir le token d'authentification")

    def completion(
        self, messages: list, model: Optional[str] = None, **kwargs
    ) -> litellm.ModelResponse:
        """Implémentation de la méthode completion pour CustomLLM"""
        print(">>> Called completion()")

        # Obtenir un token frais
        token = self.get_identity_token()

        # SIMPLIFICATION : Construction du prompt beaucoup plus simple
        # On prend simplement le dernier message utilisateur
        user_message = ""
        for msg in reversed(messages):  # Partir de la fin
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # Si on veut inclure le contexte système, on prend le premier message système
        system_context = ""
        for msg in messages:
            if msg.get("role") in ["system", "developer"]:
                system_context = msg.get("content", "")
                break

        # Construire un prompt simple
        if system_context:
            full_prompt = f"{system_context}\n\nHuman: {user_message}\n\nAssistant:"
        else:
            full_prompt = f"Human: {user_message}\n\nAssistant:"

        print(f"Prompt simplifié:\n{full_prompt}\n")

        # Préparer la requête au format Gemini
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
        }

        # Faire l'appel HTTP
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.service_url}/generateContent",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", 60),
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Réponse API: {json.dumps(result, indent=2)}")

            # Extraire le texte - version simplifiée
            try:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                # Fallback simple
                generated_text = "Erreur lors de l'extraction de la réponse"

            print(f"Texte généré: {generated_text}")

            # Créer une réponse ModelResponse
            model_response = litellm.ModelResponse()
            model_response.choices = [
                litellm.Choices(
                    message=litellm.Message(content=generated_text, role="assistant"),
                    index=0,
                    finish_reason="stop",
                )
            ]

            return model_response
        else:
            raise Exception(f"Erreur API: {response.status_code} - {response.text}")

    async def acompletion(
        self, messages: list, model: Optional[str] = None, **kwargs
    ) -> litellm.ModelResponse:
        """Version async simplifiée"""
        # Pour l'instant, on utilise la version sync
        return self.completion(messages, model, **kwargs)


# Enregistrer le handler
cloud_run_handler = CloudRunCodeLlama()
litellm.custom_provider_map = [
    {"provider": "cloud-run", "custom_handler": cloud_run_handler}
]


class CloudRunModel(LiteLlm):
    """Wrapper LiteLLM pour ADK"""

    def __init__(self, **kwargs):
        super().__init__(model="cloud-run/codellama", **kwargs)
