import asyncio
from core.orchestrator import run_agent

def main():
    print("🤖 Welcome to the AI Agent! Type 'exit' or press Ctrl+C to quit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nUse >> ")
            if not user_input.strip():
                continue
                
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye! 👋")
                break
            
            # Run async agent
            response = asyncio.run(run_agent(user_input))
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋👋👋")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
