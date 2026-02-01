import os
from dotenv import load_dotenv
from agent_graph import graph

# Load environment variables from .env file
load_dotenv()

# Check if OpenRouter API key is set
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key or api_key == "your-api-key-here":
    print("⚠️  WARNING: OPENROUTER_API_KEY not set!")
    print("Please set your OpenRouter API key:")
    print("  Windows: set OPENROUTER_API_KEY=your-key-here")
    print("  Linux/Mac: export OPENROUTER_API_KEY=your-key-here")
    print("  Or run: set_env.bat (Windows) or source set_env.sh (Linux/Mac)")
    print("  Get your API key from: https://openrouter.ai/keys")
    print()
    proceed = input("Continue anyway? (yes/no): ")
    if proceed.lower() != 'yes':
        exit(1)

# Test the agent graph with S3 bucket and paths
payload = {
    "bucket": "my-langgraph-bedrock-agent",
    "input_key": "input/input.txt",
    "output_key": "output/output.txt"
}

print("\n" + "="*60)
print("Starting agent graph execution...")
print("="*60)
print(f"📖 Reading from: s3://{payload['bucket']}/{payload['input_key']}")
print(f"📝 Writing to: s3://{payload['bucket']}/{payload['output_key']}")
print(f"🤖 LLM: OpenRouter (TNG: DeepSeek R1T2 Chimera - FREE)")
print("="*60)
print()

try:
    result = graph.invoke(payload)
    print("\n" + "="*60)
    print("✅ Execution completed successfully!")
    print("="*60)
    print(f"Result: {result}")
    print("\n📥 Check output at: s3://{payload['bucket']}/{payload['output_key']}")
except Exception as e:
    print("\n" + "="*60)
    print("❌ Execution failed!")
    print("="*60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()