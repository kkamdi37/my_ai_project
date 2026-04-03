docker run -dit --rm --name notion-mcp-server \
    --env INTERNAL_INTEGRATION_TOKEN=${NOTION_INTERNAL_INTEGRATION_TOKEN} \
    mcp/notion
