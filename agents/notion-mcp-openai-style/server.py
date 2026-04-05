import os
import json
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# ===== CONFIG =====
NOTION_TOKEN = os.getenv("INTERNAL_INTEGRATION_TOKEN")
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# =========================
# 🔧 Notion API Wrappers
# =========================

def notion_search(query):
    return requests.post(
        f"{BASE_URL}/search",
        headers=headers,
        json={"query": query, "page_size": 5}
    ).json()


def notion_get_page(page_id):
    return requests.get(
        f"{BASE_URL}/pages/{page_id}",
        headers=headers
    ).json()


def notion_get_blocks(block_id):
    return requests.get(
        f"{BASE_URL}/blocks/{block_id}/children",
        headers=headers
    ).json()


def notion_create_page(parent_id, title):
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [
                    {"text": {"content": title}}
                ]
            }
        }
    }
    return requests.post(f"{BASE_URL}/pages", headers=headers, json=payload).json()


def notion_update_page(page_id, title=None):
    payload = {}
    if title:
        payload["properties"] = {
            "title": {
                "title": [
                    {"text": {"content": title}}
                ]
            }
        }

    return requests.patch(
        f"{BASE_URL}/pages/{page_id}",
        headers=headers,
        json=payload
    ).json()


def notion_append_block(block_id, content):
    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": content}}
                    ]
                }
            }
        ]
    }

    return requests.patch(
        f"{BASE_URL}/blocks/{block_id}/children",
        headers=headers,
        json=payload
    ).json()


# =========================
# 🧠 TOOL REGISTRY (IMPORTANT)
# =========================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "notion_search",
            "description": "Search Notion pages",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notion_get_page",
            "description": "Get page metadata",
            "parameters": {
                "type": "object",
                "properties": {
                    "page_id": {"type": "string"}
                },
                "required": ["page_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notion_get_blocks",
            "description": "Get page content",
            "parameters": {
                "type": "object",
                "properties": {
                    "block_id": {"type": "string"}
                },
                "required": ["block_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notion_create_page",
            "description": "Create a new page",
            "parameters": {
                "type": "object",
                "properties": {
                    "parent_id": {"type": "string"},
                    "title": {"type": "string"}
                },
                "required": ["parent_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notion_update_page",
            "description": "Update page title",
            "parameters": {
                "type": "object",
                "properties": {
                    "page_id": {"type": "string"},
                    "title": {"type": "string"}
                },
                "required": ["page_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notion_append_block",
            "description": "Append content to a page",
            "parameters": {
                "type": "object",
                "properties": {
                    "block_id": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["block_id", "content"]
            }
        }
    }
]


# =========================
# 🔧 TOOL EXECUTOR
# =========================

def execute_tool(name, args):
    if name == "notion_search":
        return notion_search(args["query"])

    elif name == "notion_get_page":
        return notion_get_page(args["page_id"])

    elif name == "notion_get_blocks":
        return notion_get_blocks(args["block_id"])

    elif name == "notion_create_page":
        return notion_create_page(args["parent_id"], args["title"])

    elif name == "notion_update_page":
        return notion_update_page(args["page_id"], args.get("title"))

    elif name == "notion_append_block":
        return notion_append_block(args["block_id"], args["content"])

    return {"error": "Unknown tool"}


# =========================
# 🧠 OpenAI/Ollama endpoint
# =========================

@app.post("/v1/chat/completions")
async def chat_completions(req: Request):
    body = await req.json()

    # 👇 Pass tools to model
    if body.get("tools") is None:
        body["tools"] = TOOLS
    #print( f'{body=}' )

    # 👇 Call Ollama (or your LLM endpoint)
    ollama_resp = requests.post(
        "http://172.17.0.1:11434/v1/chat/completions",
        json=body
    ).json()
    #print( f'{ollama_resp=}' )

    message = ollama_resp["choices"][0]["message"]
    #print( f'{message=}' )

    # =========================
    # 🔥 HANDLE TOOL CALLS
    # =========================
    if "tool_calls" in message:
        results = []

        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])

            tool_result = execute_tool(name, args)
            results.append({
                "tool": name,
                "result": tool_result
            })

        # 👇 IMPORTANT: return as assistant (NOT tool role)
        return {
            "id": "chatcmpl-tool",
            "object": "chat.completion",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(results, indent=2)
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }

    # 👇 Normal response
    return ollama_resp
