#!/bin/env python3

import requests
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen3.5"
#MODEL = "gemma3"

# Ask chatbot
def ask_chatbot(prompt):
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]


# CLI
if __name__ == "__main__":
    print("Type 'exit' to quit\n")

    while True:
        q = input("Question: ")
        if q.lower() in ["exit", "quit"]: break

        answer = ask_chatbot(q)
        print(f"Bot: {answer}\n")
