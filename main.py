from client.llm_client import LLMClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
async def main():
    llm_client = LLMClient()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    await llm_client.chat_completion(messages=messages, stream=False, model="allenai/molmo-2-8b:free")
    print("Chat completion done.")
    await llm_client.close_client()
    
if __name__ == "__main__":
    asyncio.run(main())
    