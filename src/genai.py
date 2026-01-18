from dotenv import load_dotenv
import os
import json

from google import genai
from google.genai import types
from datetime import datetime

def get_calendar_json(user_message: str):
    # transform user calendar input into a json

    # get genai api key
    google_ai_api_key = os.getenv('GOOGLE_AI_API_KEY')

    # create genai client
    client = genai.Client(api_key=google_ai_api_key)

    # create prompt
    prompt = f"""
    Sei un assistente calendario. 
    Oggi è {datetime.now().strftime('%d/%m/%Y')}. 
    Fuso orario utente: Europe/Rome (Italia). 
    Analizza il messaggio: {user_message}. 
    Restituisci un JSON RAW valido con: 
        1. 'summary': Titolo evento. 
        2. 'startDate': Data inizio ISO 8601. 
        3. 'endDate': Data fine ISO 8601. 
        4. 'colorId': scegli l'ID in base alla categoria: 
            '11' (Rosso) se riguarda l'Avis, 
            '1' (Lavanda) se riguarda Oratorio o Chiesa, 
            '10' (Verde) se riguarda Piante, 
            '8' (Grigio) se riguarda Scuola, 
            '5' (Giallo) se riguarda Social, 
            '6'(Arancione) per tutto il resto. 
    
    IMPORTANTE: 
    - Restituisci SOLO la stringa JSON pura. 
    - NON usare backticks (''') o markdown. 
    - NON scrivere la parola 'json' all'inizio.
    """
    
    # generate json file

    response = client.models.generate_content(
        # model used
        model='gemini-2.5-flash',
        # prompt
        contents=types.Part.from_text(text=prompt)
    )

    # close connection
    client.close()

    response = json.loads(response.text.strip())

    print(response)

    # send back json to bot
    return response