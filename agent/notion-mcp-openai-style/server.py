import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

NOTION_TOKEN = os.getenv("INTERNAL_INTEGRATION_TOKEN")
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# 🔧 Notion search
def notion_search(query):
    return requests.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json={"query": query, "page_size": 5}
    ).json()


# 🧠 OpenAI-compatible endpoint
@app.post("/v1/chat/completions")
async def chat_completions(req: Request):
    body = await req.json()

    messages = body.get("messages", [])
    last_message = messages[-1]["content"]

    # 🔥 VERY SIMPLE tool routing (you can improve later)
    if "search" in last_message.lower():
        result = notion_search(last_message)

        return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": str(result)
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }

    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "No tool used."
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }
