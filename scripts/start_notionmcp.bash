echo "⚠️  You should run command below in terminal since sudo command forget your environment variable(NOTION_INTERNAL_INTEGRATION_TOKEN)"
echo

echo sudo docker run -dit --rm --name notion-mcp-server \
    --publish 8000:8000 \
    --env HOST=0.0.0.0 \
    --env INTERNAL_INTEGRATION_TOKEN=${NOTION_INTERNAL_INTEGRATION_TOKEN} \
    --env NOTION_TOKEN=${NOTION_INTERNAL_INTEGRATION_TOKEN} \
    --env NOTION_API_KEY=${NOTION_INTERNAL_INTEGRATION_TOKEN} \
    mcp/notion
