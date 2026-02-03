from dotenv import load_dotenv
import os
import google.generativeai as genai
import traceback

load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("WARNING: Gemini API Key is still the placeholder.")
        GEMINI_API_KEY = None
    else:
        print(f"DEBUG: API Key loaded: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:] if len(GEMINI_API_KEY) > 8 else ''}")
        genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

import json

# Persistent cache file
CACHE_FILE = os.path.join(os.path.dirname(__file__), "ai_cache.json")

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")

# Load initial cache
ai_response_cache = load_cache()

def get_heuristic_fallback(query: str, language: str) -> str:
    """Returns a pre-defined safety tip if the AI is completely unavailable."""
    tips = {
        "seismic": "Ensure your structure uses a flexible core or base isolation to handle shifts.",
        "wind": "Aerodynamic shaping, like tapering or twisting, significantly reduces wind load.",
        "flood": "Elevate critical infrastructure and use water-resistant materials for lower levels.",
        "default": "Always prioritize structural flexibility and use sensor-based monitoring for high-rise safety."
    }
    
    query_lower = query.lower()
    for key in tips:
        if key in query_lower:
            return f"[Offline Tip] Since the AI is busy, here is a quick safety tip: {tips[key]}"
    
    return f"[Offline Tip] {tips['default']}"

def generate_chat_response(query: str, language: str = "English") -> str:
    """
    Generates a response from the Gemini model based on the user's query and preferred language.
    Includes persistent caching and smart model fallback to handle tight quotas.
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API key is missing. Please configure the backend."

    # Check cache first
    cache_key = f"{query.lower().strip()}_{language.lower()}"
    if cache_key in ai_response_cache:
        print(f"DEBUG: Serving cached response for query: '{query[:20]}...'")
        return ai_response_cache[cache_key]

    # Models to try in order (Flash variants usually have better free tier stability)
    models_to_try = [
        os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]
    
    max_retries = 3
    
    for model_name in models_to_try:
        retry_delay = 2
        for attempt in range(max_retries):
            try:
                print(f"DEBUG: Attempting AI response with model: {model_name} (Attempt {attempt+1})")
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""
                You are 'StrataBot', a friendly and helpful AI assistant for the 'StrataMind' application.
                
                User Query: {query}
                
                Guidelines:
                1. **Tone**: Be warm, approachable, and helpful. 
                2. **Format**: Use bullet points for structured information. 
                3. **Length**: Strictly limit response to 5-10 lines.
                4. **Constraints**: Do NOT use emojis.
                5. **Language**: CRITICAL - The response MUST be ENTIRELY in {language}.
                6. **Role**: Help users design safe high-rise buildings (seismic, wind, floods).
                """
                
                response = model.generate_content(prompt)
                response_text = response.text
                
                # Save to cache and persist
                ai_response_cache[cache_key] = response_text
                save_cache(ai_response_cache)
                
                return response_text
            except Exception as e:
                error_str = str(e)
                # If quota error, handle it
                if "429" in error_str:
                    # Look for retry delay in error message if possible
                    import re
                    wait_match = re.search(r"retry in (\d+\.?\d*)s", error_str)
                    wait_time = float(wait_match.group(1)) if wait_match else retry_delay
                    
                    if attempt < max_retries - 1:
                        print(f"WARNING: Rate limit on {model_name}. Waiting {wait_time}s and retrying...")
                        import time
                        time.sleep(min(wait_time, 10)) # capping wait time for responsiveness
                        retry_delay *= 2
                        continue
                    else:
                        print(f"WARNING: Model {model_name} exhausted. Trying next model...")
                        break # Try next model
                
                print(f"Error with model {model_name}: {e}")
                break # Try next model
    
    # If all models fail, return a heuristic fallback instead of an error string
    return get_heuristic_fallback(query, language)
