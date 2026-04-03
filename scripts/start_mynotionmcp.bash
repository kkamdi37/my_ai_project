echo "⚠️  You should run command below in terminal since sudo command forget your environment variable(NOTION_INTERNAL_INTEGRATION_TOKEN)"
echo

echo sudo docker run -dit --rm --name my-notionmcp \
    --publish 8000:8000 \
    --env INTERNAL_INTEGRATION_TOKEN=${NOTION_INTERNAL_INTEGRATION_TOKEN} \
    notion-mcp-server
