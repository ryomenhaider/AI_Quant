import asyncio
import json

from app.services.llm import LLMService


async def main():
    print("=" * 60)
    print("Testing LLM Tool Orchestration")
    print("=" * 60)

    llm = LLMService()

    test_messages = [
        "What is the Sharpe ratio for returns [0.01, -0.02, 0.03]?",
    ]

    for msg in test_messages:
        print(f"\nUser: {msg}")
        print("-" * 40)

        response = await llm.chat(msg)

        print(f"LLM Response: {response}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
