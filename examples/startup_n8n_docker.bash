#!/bin/bash

mkdir -p ~/workspace/n8n/n8n_data
N8N_ENCRYPTION_KEY=`openssl rand -hex 24`

sudo docker run -it --rm --name n8n --publish 5678:5678 \
  --env N8N_SECURE_COOKIE=false \
  --env N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY} \
  --volume ~/workspace/n8n/n8n_data:/home/node/.n8n \
  n8nio/n8n
