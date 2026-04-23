FROM ubuntu

RUN apt update
RUN apt install -y curl jq
RUN curl -fsSL https://opencode.ai/install | bash
COPY utils/run_me_for_connecting_gemma4_in_ollama /root/utils/
