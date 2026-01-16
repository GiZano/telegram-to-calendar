from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from datetime import datetime

# load environment variables from .env file
load_dotenv()

# load google ai api key from .env file
google_ai_api_key = os.getenv("GOOGLE_AI_API_KEY")

# create genai client
client = genai.Client(api_key=google_ai_api_key)

# SandBox user message
user_message = "Evento: GIP (oratorio/chiesa), inizio: oggi 18:45, fine: oggi: 23:00"

# Prompt creation
prompt = f"Sei un assistente calendario. Oggi è {datetime.now().strftime('%d/%m/%Y')}. Fuso orario utente: Europe/Rome (Italia). Analizza il messaggio: {user_message}. Restituisci un JSON RAW valido con: 1. 'summary': Titolo evento. 2. 'startDate': Data inizio ISO 8601. 3. 'endDate': Data fine ISO 8601. 4. 'colorId': scegli l'ID in base alla categoria: '11' (Rosso) se riguarda l'Avis, '1' (Lavanda) se riguarda Oratorio o Chiesa, '10' (Verde) se riguarda Piante, '8' (Grigio) se riguarda Scuola, '5' (Giallo) se riguarda Social, '6'(Arancione) per tutto il resto. IMPORTANTE: Restituisci SOLO la stringa JSON pura. NON usare backticks (''') o markdown. NON scrivere la parola 'json' all'inizio."

# generate content
response = client.models.generate_content(
    # model to use
    model='gemini-2.5-flash',
    # prompt to use
    contents=types.Part.from_text(text=prompt)
)

print(response.text)

# close session
client.close()