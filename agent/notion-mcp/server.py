import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# 🔑 Config
NOTION_TOKEN = os.getenv("INTERNAL_INTEGRATION_TOKEN")
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# ---------------------------
# 🔧 Notion API Wrappers
# ---------------------------

def notion_search(query, page_size=5):
    url = f"{BASE_URL}/search"
    payload = {"query": query, "page_size": page_size}
    return requests.post(url, headers=headers, json=payload).json()


def notion_get_page(page_id):
    url = f"{BASE_URL}/pages/{page_id}"
    return requests.get(url, headers=headers).json()


def notion_get_blocks(block_id):
    url = f"{BASE_URL}/blocks/{block_id}/children"
    return requests.get(url, headers=headers).json()


def notion_create_page(parent_id, title):
    url = f"{BASE_URL}/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": [
                {
                    "text": {"content": title}
                }
            ]
        }
    }
    return requests.post(url, headers=headers, json=payload).json()


# ---------------------------
# 🧠 MCP Dispatcher
# ---------------------------

@app.post("/mcp")
async def mcp_endpoint(req: Request):
    body = await req.json()

    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    try:
        # 🔍 Search
        if method == "notion.search":
            result = notion_search(params.get("query", ""))

        # 📄 Get page metadata
        elif method == "notion.get_page":
            result = notion_get_page(params["page_id"])

        # 📚 Get page content
        elif method == "notion.get_blocks":
            result = notion_get_blocks(params["block_id"])

        # ✏️ Create page
        elif method == "notion.create_page":
            result = notion_create_page(
                params["parent_id"],
                params["title"]
            )

        # 📦 Tool discovery (VERY useful for MCP clients)
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "notion.search",
                        "description": "Search Notion pages",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "notion.get_page",
                        "description": "Get page metadata",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "page_id": {"type": "string"}
                            },
                            "required": ["page_id"]
                        }
                    },
                    {
                        "name": "notion.get_blocks",
                        "description": "Get page content blocks",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "block_id": {"type": "string"}
                            },
                            "required": ["block_id"]
                        }
                    },
                    {
                        "name": "notion.create_page",
                        "description": "Create a new page",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "parent_id": {"type": "string"},
                                "title": {"type": "string"}
                            },
                            "required": ["parent_id", "title"]
                        }
                    }
                ]
            }

        else:
            raise ValueError(f"Unknown method: {method}")

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }
