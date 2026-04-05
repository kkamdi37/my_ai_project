# 🧪 Test it
curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "notion.search",
    "params": {"query": "meeting notes"}
  }'


curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "notion.update_page",
    "params": {
      "page_id": "[YOUR_PAGE_ID_HERE]",
      "title": "Updated Title 🚀"
    }
  }'


curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "notion.append_block",
    "params": {
      "block_id": "[YOUR_PAGE_ID_HERE]",
      "content": "This was added via MCP!"
    }
  }'
