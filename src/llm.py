import asyncio
import logging
from collections.abc import Sequence

from ollama import AsyncClient

from config import BASE_MODEL, HOST

logger = logging.getLogger(__name__)

__all__ = ["run_prompt", "run_prompts", "check_host"]


def _client() -> AsyncClient:
    return AsyncClient(host=HOST)


async def _chat(client: AsyncClient, prompt: str, model: str) -> str: 
    message = {"role": "user", "content": prompt}
    response = await client.chat(
        model=model,
        messages=[message],
        stream=False,
    )
    return response["message"]["content"].strip()


async def run_prompt(prompt: str, *, model: str = BASE_MODEL) -> str:
    async with _client() as client:
        return await _chat(client, prompt, model)


async def run_prompts(prompts: Sequence[str], *, model: str = BASE_MODEL) -> list[str]:
    if not prompts:
        return []
    async with _client() as client:
        return await asyncio.gather(
            *(_chat(client, prompt, model) for prompt in prompts)
        )


async def check_host() -> bool:
    try:
        async with _client() as client:
            await client.list()
    except Exception:
        logger.warning("Ollama host %s is unavailable", HOST, exc_info=True)
        return False
    return True
