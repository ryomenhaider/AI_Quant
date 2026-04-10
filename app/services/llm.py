import json
import logging
from typing import Any, Optional

import httpx
from app.core.config import config
from app.services.tool_registry import TOOLS
from app.services.tool_executor import execute_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TOOL_CALLS = 3

SYSTEM_PROMPT = """You are a quantitative analyst.

You have access to tools for market data and risk calculations.

RULES:
* You MUST use tools for any data request
* You MUST NOT calculate manually
* If data is required → call a tool
* After receiving tool results → explain clearly and professionally"""


class LLMService:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemma-2-9b-it"
        self.system_prompt = SYSTEM_PROMPT

    async def chat(self, message: str) -> Any:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message},
        ]

        response = await self._make_request(messages)
        return response.get("content", str(response))

    async def _make_request(self, messages: list[dict]) -> str:
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]

    def _extract_tool_calls(self, message: dict) -> Optional[list[dict]]:
        if "tool_calls" not in message:
            return None

        tool_calls = []
        for tc in message["tool_calls"]:
            func = tc.get("function", {})
            try:
                args = json.loads(func.get("arguments", "{}"))
            except json.JSONDecodeError:
                args = {}

            tool_calls.append(
                {"id": tc.get("id"), "name": func.get("name"), "arguments": args}
            )

        return tool_calls
