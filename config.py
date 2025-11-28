import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

def get_gemini_client():
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    if API_KEY.strip() != API_KEY:
        print("Warning: API key may have leading/trailing whitespace")
    
    return OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

gemini_client = None

def initialize_client():
    global gemini_client
    if gemini_client is None:
        gemini_client = get_gemini_client()
    return gemini_client
