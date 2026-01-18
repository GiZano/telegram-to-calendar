from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# load google ai api key from .env file
google_ai_api_key = os.getenv("GOOGLE_AI_API_KEY")

# create genai client
client = genai.Client(api_key=google_ai_api_key)

# generate content
response = client.models.generate_content(
    # model to use
    model='gemini-2.5-flash',
    # Test prompt for basic math operation
    contents=types.Part.from_text(text='What is 2 + 2?'),
)

print(response.text)

# close session
client.close()