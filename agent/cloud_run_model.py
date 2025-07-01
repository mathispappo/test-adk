import google.auth
import google.oauth2.id_token
import google.auth.transport.requests
from google.adk.models.lite_llm import LiteLlm
import requests
import json
import litellm
from typing import Optional
from litellm import CustomLLM
import asyncio
import subprocess


class CloudRunCodeLlama(CustomLLM):
    """Custom LLM handler pour Cloud Run"""

    def __init__(self):
        self.service_url = "http://34.107.178.200"
        self.request = google.auth.transport.requests.Request()

    def get_identity_token(self) -> str:
        """Obtenir un token d'identité Google valide"""
        try:
            # Utiliser directement gcloud CLI qui fonctionne bien d'après les tests
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

        # Construire le prompt complet en combinant tous les messages
        # Les messages sont typiquement [{"role": "system/developer", "content": "..."}, {"role": "user", "content": "..."}]
        full_prompt = ""

        print(messages)

        for msg in messages:
            # Concatenation des messages
            role = msg.get("role", "user")
            content = msg.get("content", "")
            full_prompt += f"{role.capitalize()}: {content}\n"
        print(f"Prompt complet avant traitement:\n{full_prompt}\n\n")

        # for msg in messages:
        #     role = msg.get("role", "user")
        #     content = msg.get("content", "")

        #     if role in ["system", "developer"]:
        #         # Ajouter l'instruction système au début
        #         if not full_prompt:  # Seulement si c'est le premier message
        #             full_prompt += f"System: {content}\n\n"
        #     elif role == "user":
        #         # Ajouter la requête utilisateur
        #         if full_prompt and not full_prompt.endswith("\n\n"):
        #             full_prompt += "\n\n"
        #         full_prompt += f"Human: {content}\n\nAssistant:"
        #     elif role == "assistant":
        #         # Si on a des messages précédents de l'assistant
        #         full_prompt += f" {content}"

        # Préparer la requête au format Gemini avec un seul message contenant tout le contexte
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "max_output_tokens": kwargs.get("max_tokens", 512),
                "temperature": kwargs.get("temperature", 0.7),
            },
        }
        print(f"Payload envoyé à l'API:\n{json.dumps(payload, indent=2)}\n\n")

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
            print(f"Réponse complète de l'API: {json.dumps(result, indent=2)}")

            # Extraire le texte de la réponse - vérifier la structure
            try:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                print(f"Erreur lors de l'extraction du texte: {e}")
                print(f"Structure de la réponse: {result}")
                # Essayer une extraction alternative
                if "text" in result:
                    generated_text = result["text"]
                elif "response" in result:
                    generated_text = result["response"]
                else:
                    generated_text = str(result)

            print(f"Texte généré extrait: {generated_text}")

            # Créer une réponse ModelResponse de LiteLLM
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
        """Implémentation async de completion"""
        print(">>> Called acompletion()")
        # Pour l'instant, on utilise la version sync dans un executor
        loop = asyncio.get_event_loop()

        # run_in_executor ne peut pas prendre de kwargs, on doit créer une fonction partielle
        from functools import partial

        completion_func = partial(self.completion, messages, model, **kwargs)

        return await loop.run_in_executor(None, completion_func)


# Enregistrer le custom handler
cloud_run_handler = CloudRunCodeLlama()
litellm.custom_provider_map = [
    {"provider": "cloud-run", "custom_handler": cloud_run_handler}
]


class CloudRunModel(LiteLlm):
    """Wrapper LiteLLM pour ADK"""

    def __init__(self, **kwargs):
        # Configuration pour utiliser notre custom provider
        super().__init__(model="cloud-run/codellama", **kwargs)
