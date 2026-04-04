# 🧪 Basic curl test for ollama docker
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4",
    "messages": [{"role": "user", "content": "hi"}]
  }'

# 🧪 Basic curl test (OpenAI-style)
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "model": "gemma4",
  "messages": [
    {
      "role": "user",
      "content": "search my notion for meeting notes"
    }
  ]
}'

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4",
    "messages": [
      {
        "role": "user",
        "content": "Update the Notion page title to \"Updated via MCP\". Page ID is [YOUR_PAGE_ID_HERE]"
      }
    ],
    "tool_choice": {
      "type": "function",
      "function": {
        "name": "notion_update_page"
      }
    }
  }'
