import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import SYSTEM_PROMPT

#Load envyronment variables
load_dotenv()

client = genai.Client()

def printHelloWorld():
    """Print a Hello World and confirm execution"""
    print("Hello World")
    return "printHelloWorld has been executed"


def run_agent(user_query):
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {user_query}"
    
    response = client.models.generate_content(
        model='gemma-3-27b-it',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            temperature=0.1 # Muy bajo para evitar alucinaciones
        )
    )

    try:
        # Limpiamos posibles espacios o saltos de línea
        raw_text = response.text.strip()
        
        # Eliminar bloques de código markdown si el modelo los genera
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        raw_text = raw_text.strip()
        
        data = json.loads(raw_text)
        
        # Lógica de Dispatcher
        if data.get("FunctionCalling") and data["FunctionCalling"].get("name"):
            func_name = data["FunctionCalling"]["name"]
            attrs = data["FunctionCalling"].get("attributes", {})
            
            print(f"Agente llamó a la función: {func_name}")
            
            if func_name == "hello_world":
                result = printHelloWorld()
                return f"Internal Result: {result}"
            else:
                return f"Error: Función desconocida '{func_name}'"
        
        elif data.get("text"):
            return f"Agente dice: {data['text']}"
        
        else:
             return "Error: Respuesta del modelo no sigue el esquema esperado (ni FunctionCalling ni text)."
            
    except json.JSONDecodeError as e:
        print(f"Error parseando el JSON: {e}")
        print(f"Respuesta cruda del modelo: {response.text}")
        return "Error de formato JSON."
    except Exception as e:
        print(f"Error inesperado: {e}")
        return "Error del sistema."

if __name__ == "__main__":
    response_text = run_agent("What are you?")
    print(response_text)
