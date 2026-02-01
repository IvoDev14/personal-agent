import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

def get_client():
    """Initializes and returns the Google GenAI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
    
    # Client initialization might not explicitly need the key passed if it picks up from env, 
    # but strictly following the SDK usage often implies just `genai.Client()`.
    # Based on previous code: `client = genai.Client()`
    return genai.Client(api_key=api_key) if api_key else genai.Client()
