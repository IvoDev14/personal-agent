import asyncio
from core.orchestrator import Orchestrator

async def main():
    print("🤖 Welcome to the AI Agent! Type 'exit' or press Ctrl+C to quit.")
    print("-" * 50)
    
    orchestrator = Orchestrator()
    await orchestrator.start()
    
    try:
        while True:
            user_input = input("\nUse >> ")
            if not user_input.strip():
                continue
                
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            # Run async agent
            response = await orchestrator.process_query(user_input)
            print(f"\n{response}")
            
    except KeyboardInterrupt:
        print("\n\nUser interrupted.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        print("Goodbye! 👋")
        await orchestrator.stop()

if __name__ == "__main__":
    asyncio.run(main())
