import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_API_URL ="https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

print("Token backend :", HUGGINGFACE_TOKEN)

def get_ai_response(prompt: str):
    payload = {"inputs": prompt}

    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        print("Status code:", response.status_code)
        print("Réponse brute:", response.text)

        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data[0].get("generated_text", "").strip()
            clean_response = generated_text.replace(prompt, "").strip()
            return clean_response if clean_response else "Réponse vide de l'IA."
        else:
            return f"Erreur IA : {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erreur de requête : {str(e)}"
