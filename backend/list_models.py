import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

print("Listing available models...")
try:
    with open("clean_models.txt", "w", encoding="utf-8") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"MODEL: {m.name}")
                f.write(f"{m.name}\n")
except Exception as e:
    print(f"Error listing models: {e}")
