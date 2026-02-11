import json
import asyncio
import pathlib
import os
from google.genai import types
from config.prompts import SYSTEM_PROMPT
from core.client import get_client
from core.mcp_client import MCPClientManager

client = get_client()

async def run_agent(user_query):
    """
    Executes the agent's ReAct loop with MCP support using Text-Based JSON.
    """
    
    MAX_STEPS = 10
    messages = []
    
    # Initialize MCP Manager
    mcp_manager = MCPClientManager()
    
    try:
        # Dynamic MCP Server Loading
        modules_path = pathlib.Path("modules")
        if not modules_path.exists():
            print("⚠️ 'modules' directory not found.")
        else:
            for module_dir in modules_path.iterdir():
                if module_dir.is_dir():
                    mcp_config = module_dir / "mcp.json"
                    if mcp_config.exists():
                        try:
                            with open(mcp_config, "r") as f:
                                config = json.load(f)
                                
                            command = config.get("command")
                            args = config.get("args", [])
                            
                            if command:
                                await mcp_manager.connect_to_server(
                                    module_dir.name, 
                                    command, 
                                    args
                                )
                            else:
                                print(f"⚠️ Warning: 'command' missing in {mcp_config}")
                                
                        except json.JSONDecodeError:
                             print(f"❌ Error: Invalid JSON in {mcp_config}")
                        except Exception as e:
                            print(f"❌ Error loading module {module_dir.name}: {e}")
                    else:
                        print(f"ℹ️ Skipping {module_dir.name}: No mcp.json found.")
        
        # Get Tools and Format for Prompt
        mcp_tools = await mcp_manager.list_tools()
        formatted_tools = format_tools_for_prompt(mcp_tools)
        
        # Inject tools into System Prompt
        system_instruction = SYSTEM_PROMPT.format(tool_definitions=formatted_tools)
            
        # Initialize the conversation
        # Note: No 'tools=' in config, we are doing it manually via text
        chat_session = client.chats.create(
            model='gemma-3-27b-it',
            config=types.GenerateContentConfig(
                temperature=0.1 
            ),
            history=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=system_instruction)]
                ),
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="I understand. I am ready to act as the function-calling agent using JSON.")]
                )
            ]
        )
        
        # Send the actual user query
        response = chat_session.send_message(user_query)
        
        step = 0
        while step < MAX_STEPS:
            step += 1
            
            try:
                # Parse Text Response
                raw_text = clean_response(response.text)
                
                # Try to parse JSON
                try:
                    data = json.loads(raw_text)
                except json.JSONDecodeError:
                    print(f"❌ JSON Error. Raw: {response.text}")
                    # Feedback to model to fix JSON
                    response = chat_session.send_message("SYSTEM ERROR: Invalid JSON format. Please output strictly valid JSON.")
                    continue

                # CASE A: Function Call
                if data.get("FunctionCalling") and data["FunctionCalling"].get("name"):
                    func_name = data["FunctionCalling"]["name"]
                    attrs = data["FunctionCalling"].get("attributes", {})
                    
                    print(f"🔄 Agent requires action: {func_name} with args: {attrs}")
                    
                    # Execute via MCP
                    try:
                        result = await mcp_manager.call_tool(func_name, attrs)
                        
                        # Format observation from MCP result
                        observation = ""
                        if result.content:
                            for content in result.content:
                                if content.type == "text":
                                    observation += content.text
                                    
                        print(f"   -> Observation: {observation}")
                        
                        # Feed result back per ReAct loop
                        response = chat_session.send_message(f"OBSERVATION: {observation}")
                        continue
                        
                    except Exception as e:
                        error_msg = f"Tool execution failed: {str(e)}"
                        print(f"❌ {error_msg}")
                        response = chat_session.send_message(f"SYSTEM ERROR: {error_msg}")
                        continue

                # CASE B: Final Answer
                elif data.get("text"):
                    return f"Agent says: {data['text']}"
                
                else:
                    # Ambiguous response, force retry
                    response = chat_session.send_message("SYSTEM ERROR: Invalid JSON format. Missing 'FunctionCalling' or 'text'.")
                    
            except Exception as e:
                return f"Critical System Error during ReAct loop: {e}"

    finally:
        await mcp_manager.cleanup()
            
    return "Agent reached maximum steps without a final answer."

def format_tools_for_prompt(tools):
    """Formats MCP tools into a JSON-like schema string for the prompt."""
    tool_list = []
    for t in tools:
        tool_def = {
            "name": t.name,
            "description": t.description,
            "attributes": t.inputSchema.get("properties", {}),
            "required_attributes": t.inputSchema.get("required", [])
        }
        tool_list.append(tool_def)
    
    return json.dumps({"tools": tool_list}, indent=2)

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

