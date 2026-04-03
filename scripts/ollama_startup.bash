docker run -dit --rm --name my-ollama \
    --env OLLAMA_HOST=0.0.0.0 \
    --publish 11434:11434 \
    --volume ~/workspace/experiment/ollama_data:/root/.ollama \
    ollama/ollama
