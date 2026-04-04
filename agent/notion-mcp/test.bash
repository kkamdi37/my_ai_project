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
      "page_id": "3373ae85-3486-807d-82c3-ec2a8ddfa259",
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
      "block_id": "3373ae85-3486-807d-82c3-ec2a8ddfa259",
      "content": "This was added via MCP!"
    }
  }'
