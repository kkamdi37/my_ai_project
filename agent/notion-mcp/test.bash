# 🧪 Test it
curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "notion.search",
    "params": {"query": "meeting notes"}
  }'
