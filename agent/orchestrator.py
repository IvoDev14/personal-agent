import json
from google.genai import types
from config.prompts import SYSTEM_PROMPT
from tools.basic_tools import printHelloWorld
from agent.client import get_client

client = get_client()

def run_agent(user_query):
    """
    Executes the agent's ReAct loop.
    
    1. Sends user query to model.
    2. Model decides to call a function or answer.
    3. If function: Execute -> Feed result back -> Repeat.
    4. If text: Return answer.
    """
    
    MAX_STEPS = 10
    messages = []
    
    # Initialize the conversation
    chat_session = client.chats.create(
        model='gemma-3-27b-it',
        config=types.GenerateContentConfig(
            temperature=0.1 # Low temp for deterministic logic
        ),
        history=[
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=SYSTEM_PROMPT)]
            ),
            types.Content(
                role="model",
                parts=[types.Part.from_text(text="I understand. I am ready to act as the function-calling agent.")]
            )
        ]
    )
    
    # Send the actual user query
    response = chat_session.send_message(user_query)
    
    step = 0
    while step < MAX_STEPS:
        step += 1
        
        try:
            # Parse Response
            raw_text = clean_response(response.text)
            data = json.loads(raw_text)
            
            # CASE A: Function Call
            if data.get("FunctionCalling") and data["FunctionCalling"].get("name"):
                func_name = data["FunctionCalling"]["name"]
                print(f"🔄 Agent requires action: {func_name}")
                
                # Execute Tool
                observation = execute_tool(func_name)
                
                # Feedback to Model
                print(f"   -> Observation: {observation}")
                response = chat_session.send_message(f"OBSERVATION: {observation}")
                continue # Loop again with new response
            
            # CASE B: Final Answer
            elif data.get("text"):
                return f"Agent says: {data['text']}"
            
            else:
                # Ambiguous response, force retry
                response = chat_session.send_message("SYSTEM ERROR: Invalid JSON format. missing 'FunctionCalling' or 'text'.")
                
        except json.JSONDecodeError:
            print(f"❌ JSON Error. Raw: {response.text}")
            response = chat_session.send_message("SYSTEM ERROR: Verify your JSON syntax.")
        except Exception as e:
            return f"Critical System Error: {e}"

    return "Agent reached maximum steps without a final answer."

def clean_response(text):
    """Helper to strip markdown code blocks from JSON."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def execute_tool(name):
    """Dispatcher for tools."""
    if name == "hello_world":
        return printHelloWorld()
    return f"Error: Tool '{name}' not found."
