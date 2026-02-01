import json
from google.genai import types
from config.prompts import SYSTEM_PROMPT
from tools.basic_tools import printHelloWorld
from agent.client import get_client

client = get_client()

def run_agent(user_query):
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {user_query}"
    
    response = client.models.generate_content(
        model='gemma-3-27b-it',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            temperature=0.1 # Very low to avoid hallucinations
        )
    )

    try:
        # Clean potential spaces or line breaks
        raw_text = response.text.strip()
        
        # Remove markdown code blocks if the model generates them
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        raw_text = raw_text.strip()
        
        data = json.loads(raw_text)
        
        # Dispatcher Logic
        if data.get("FunctionCalling") and data["FunctionCalling"].get("name"):
            func_name = data["FunctionCalling"]["name"]
            attrs = data["FunctionCalling"].get("attributes", {})
            
            print(f"Agent called function: {func_name}")
            
            if func_name == "hello_world":
                result = printHelloWorld()
                return f"Internal Result: {result}"
            else:
                return f"Error: Unknown function '{func_name}'"
        
        elif data.get("text"):
            return f"Agent says: {data['text']}"
        
        else:
             return "Error: Model response does not follow the expected schema (neither FunctionCalling nor text)."
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw model response: {response.text}")
        return "JSON format error."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "System error."
