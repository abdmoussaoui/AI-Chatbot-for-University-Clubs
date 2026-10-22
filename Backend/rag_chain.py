import json
import os
import re
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

# --- 1. SETUP - Initialisation des variables globales à None ---
ALL_CLUBS = []
VECTOR_STORE = None
LLM = None
RAG_CHAIN = None

class OpenRouterLLM:
    """Custom LLM class for OpenRouter API."""
    def __init__(self, api_key, model="mistralai/mistral-7b-instruct:free", temperature=0.3, max_tokens=512):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("SITE_URL", "http://localhost"),
            "X-Title": os.getenv("SITE_NAME", "FSBM Club Assistant")
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def make_api_call(self, payload):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=120)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            print(f"OpenRouter API error: {e.response.status_code} {e.response.text}")
            raise

    def __call__(self, prompt):
        # Convert prompt to string
        prompt = str(prompt)  # Ensure prompt is a string
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        response = self.make_api_call(payload)
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing OpenRouter response: {e}\nResponse: {response.text}")
            raise

def load_all_models():
    """Cette fonction est appelée par FastAPI pour charger tous les modèles au démarrage."""
    global ALL_CLUBS, VECTOR_STORE, LLM, RAG_CHAIN

    print("--- Chargement des modèles et création du vector store ---")

    try:
        # Charger les données des clubs
        with open("data/clubs.json", "r", encoding="utf-8") as f:
            ALL_CLUBS = json.load(f)["clubs"]

        # Créer les documents pour le vector store
        documents = [Document(page_content=club["description"], metadata={"name": club["name"]}) for club in ALL_CLUBS]
        
        # Use HuggingFaceEmbeddings from langchain-huggingface
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        VECTOR_STORE = FAISS.from_documents(documents, embeddings)

        # Initialiser OpenRouter LLM
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        print(f"Loaded OPENROUTER_API_KEY: {openrouter_api_key}")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")
        
        LLM = OpenRouterLLM(
            api_key=openrouter_api_key,
            model="mistralai/mistral-7b-instruct:free",
            temperature=0.3,
            max_tokens=512
        )

        # Définir le nouveau template de prompt avec les clubs existants et accolades échappées
        prompt_template_str = """
Tu es un expert en orientation étudiante à la FSBM. Ton rôle est d'aider les étudiants à trouver le club qui leur correspond le mieux, parmi les clubs listés ci-dessous.

== OBJECTIF ==
À partir des réponses de l'utilisateur, recommande-lui UN SEUL club de la liste fournie, avec une raison claire et pertinente.

== FONCTIONNEMENT ==
1. Analyse les réponses de l'utilisateur. Identifie ses centres d’intérêt, ses objectifs, ses préférences (technique, artistique, scientifique, social, sportif...).
2. Compare ces éléments avec les descriptions des clubs ci-dessous.
3. Recommande un club unique, accompagné d'une explication claire ("car tu aimes...", "car tu veux...").

== FORMATS DE SORTIE ==
- Si tu as suffisamment d'infos pour recommander un club :
{{
    "action": "recommend",
    "responseText": "Je te recommande le club XYZ car ...",
    "recommendation": {{
        "clubName": "nom du club",
        "reason": "brève raison claire"
    }}
}}
- Si tu n'as pas encore assez d'infos ou si la requête est vague/ambiguë :
{{
    "action": "ask",
    "responseText": "question à poser",
    "recommendation": {{
        "clubName": null,
        "reason": null
    }}
}}

== INSTRUCTIONS ==
- Pose une question claire et spécifique à chaque fois, sans répéter celles de l’historique.
- Ne fais une recommandation QUE si l'utilisateur exprime un intérêt clair et spécifique (ex : "j'aime programmer", "je veux apprendre à coder", "je veux faire du sport"). 
- Si l'utilisateur exprime une incertitude (ex : "je ne sais pas", "j'ai entendu parler de X", "je n'ai aucune idée"), pose une question pour clarifier son intérêt (ex : "Es-tu intéressé à apprendre à coder ou es-tu juste curieux à propos de la programmation ?").
- Si l'utilisateur mentionne "proche" ou "proximité", réponds : "Je n'ai pas d'infos sur la localisation des clubs, mais je peux t'aider à trouver celui qui te correspond ! Quelles activités aimes-tu ?"
- Si l'utilisateur demande un club inexistant (ex : club d’échecs), informe-le gentiment qu'il n’existe pas et propose une alternative ou pose une question.
- Si l'entrée mentionne "échec", interprète cela comme le jeu d'échecs.
- Utilise uniquement les clubs listés ci-dessous. Ne propose rien d’inventé.
- Parle à la première personne ("je te recommande", "je pense que...").
- Assure-toi que toutes les valeurs dans le JSON de sortie utilisent "null" au lieu de "None".

== LISTE DES CLUBS EXISTANTS ==
{all_clubs}

== CLUBS DISPONIBLES (PLUS PERTINENTS) ==
{retrieved_clubs}

== HISTORIQUE ==
{chat_history}

== DERNIÈRE RÉPONSE DE L'ÉTUDIANT ==
{user_query}
"""
        prompt = PromptTemplate.from_template(prompt_template_str)

        # Syntaxe LCEL pour la chaîne RAG
        RAG_CHAIN = (
            {
                "all_clubs": lambda x: x["all_clubs"],
                "retrieved_clubs": lambda x: x["retrieved_clubs"],
                "chat_history": lambda x: x["chat_history"],
                "user_query": lambda x: x["user_query"],
            }
            | prompt
            | LLM
            | StrOutputParser()
        )

        print("--- Tous les modèles ont été chargés avec succès. ---")
    except Exception as e:
        print(f"Erreur lors du chargement des modèles : {e}")
        raise

def clean_json_output(raw_output: str) -> str:
    """Nettoie la sortie brute du LLM pour extraire un JSON valide."""
    json_pattern = r'\{[\s\S]*\}'
    match = re.search(json_pattern, raw_output, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"

def get_intelligent_response(query: str, session: list[dict]):
    if not RAG_CHAIN or not VECTOR_STORE:
        return {"response": "Désolé, l'assistant IA n'est pas prêt.", "recommendation": None, "club_scores": None}

    try:
        # Limiter l'historique à 10 échanges
        session_history = session[-10:]
        # Contexte pour la recherche vectorielle
        search_context = " ".join(
            [entry.get("user_query", "") if isinstance(entry, dict) else str(entry) for entry in session_history] + [query])
        chat_history_str = "\n".join([
            f"User: {entry.get('user_query', '')}\nBot: {entry.get('response', '')}" if isinstance(entry, dict) else str(entry)
            for entry in session_history]) or "La conversation vient de commencer."

        # Effectuer une recherche de similarité
        results = VECTOR_STORE.similarity_search(search_context, k=3)
        retrieved_clubs_context = "\n\n".join(
            [f'Club: {doc.metadata["name"]}\nDescription: {doc.page_content}' for doc in results]
        )

        # Formatter la liste complète des clubs existants
        all_clubs_context = "\n\n".join(
            [f'Club: {club["name"]}\nDescription: {club["description"]}' for club in ALL_CLUBS]
        )

        # Préparer l'entrée pour la chaîne RAG
        llm_input = {
            "all_clubs": all_clubs_context,
            "retrieved_clubs": retrieved_clubs_context,
            "chat_history": chat_history_str,
            "user_query": query
        }

        # Invoquer la chaîne RAG
        llm_output_str = RAG_CHAIN.invoke(llm_input)
        print("--- LLM INPUT ---\n", llm_input, "\n--- LLM RAW OUTPUT ---\n", llm_output_str, "\n----------------------")

        # Nettoyer la sortie pour extraire le JSON
        llm_output_str = clean_json_output(llm_output_str)

        # Parser la sortie
        try:
            response_json = json.loads(llm_output_str)
        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON: {e}\nRaw output: {llm_output_str}")
            return {
                "response": "Désolé, la réponse du modèle n'est pas valide.",
                "recommendation": None,
                "club_scores": None
            }

        # Vérifier la structure de la réponse
        action = response_json.get("action")
        response_text = response_json.get("responseText")
        recommendation_details = response_json.get("recommendation", {})

        if not action or not response_text:
            print(f"Réponse JSON invalide : {response_json}")
            return {
                "response": "Désolé, la réponse du modèle est incomplète.",
                "recommendation": None,
                "club_scores": None
            }

        # Convertir None en null dans recommendation_details
        recommendation_details = {
            "clubName": recommendation_details.get("clubName", None),
            "reason": recommendation_details.get("reason", None)
        }

        # Préparer la réponse finale
        final_response = {"response": response_text, "recommendation": None, "club_scores": None}

        if action == "recommend" and recommendation_details.get("clubName"):
            club_name = recommendation_details["clubName"]
            final_response["recommendation"] = {
                "club": club_name,
                "explanation": recommendation_details.get("reason")
            }
            # Calculer les scores pour les clubs
            club_scores = {}
            for club in ALL_CLUBS:
                score_data = VECTOR_STORE.similarity_search_with_score(search_context, k=1, filter={'name': club['name']})
                if score_data:
                    similarity = max(0, 1 - score_data[0][1] / 2)  # Normalisation approximative
                    club_scores[club["name"]] = round(similarity, 2)
            final_response["club_scores"] = club_scores

        # Ajouter la réponse à l'historique pour le suivi
        session.append({"user_query": query, "response": response_text, "action": action})

        return final_response
    except Exception as e:
        print(f"Unexpected error in get_intelligent_response: {e}")
        return {
            "response": "Une erreur inattendue s'est produite.",
            "recommendation": None,
            "club_scores": None
        }