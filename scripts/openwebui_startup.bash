docker run -dit --rm --name my-openwebui \
    --publish 8080:8080 \
    --volume ~/workspace/experiment/owu_data:/app/backend/data \
    ghcr.io/open-webui/open-webui
