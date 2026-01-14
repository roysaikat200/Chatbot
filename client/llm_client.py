import os
from openai import AsyncOpenAI
from typing import Any


class LLMClient:
    def __init__(self) -> None:
        self._client: AsyncOpenAI | None = None

    def get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=os.environ.get("api_key", ""),
                base_url=os.environ.get("base_url", "https://openrouter.ai/api/v1")
            )
        return self._client

    async def close_client(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None
            
    async def chat_completion(self, 
                              messages: list[dict[str, Any]], 
                              stream: bool,
                              model: str) -> None:
        client = self.get_client()
        kwargs = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        if stream:
            await self._stream_response(client, kwargs)  # Added await
        else:
            await self._non_stream_response(client, kwargs)  # Added await
    
    async def _stream_response(self, client: AsyncOpenAI, kwargs: dict[str, Any]) -> None:
        response = await client.chat.completions.create(**kwargs)
        async for chunk in response:
            # Use attribute access instead of .get()
            content = chunk.choices[0].delta.content
            if content:  # Check if content exists
                print(content, end="")
    
    async def _non_stream_response(self, client: AsyncOpenAI, kwargs: dict[str, Any]) -> None:
        response = await client.chat.completions.create(**kwargs)
        # Use attribute access instead of dictionary access
        print(response.choices[0].message.content)