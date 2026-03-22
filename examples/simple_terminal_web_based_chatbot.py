#!/bin/env python3

import requests
from bs4 import BeautifulSoup

BRAVE_API_KEY = "YOUR_API_KEY_HERE"

OLLAMA_URL = "http://localhost:11434/api/generate"

#MODEL = "qwen3.5"
MODEL = "gemma3"


# 1-1. Web search (DuckDuckGo)
def search_web(query, num_results=3):
    url = "https://html.duckduckgo.com/html/"
    params = { "q": query }
    headers = { "User-Agent": "Mozilla/5.0" }

    res = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.select(".result__a")[:num_results]:
        title = a.get_text()
        link = a["href"]
        results.append(f"{title}\n{link}")

    return "\n\n".join(results)

# 1-2. Web search by brave search API
def brave_search(query, num_results=3):
    url = "https://api.search.brave.com/res/v1/web/search"
    params = { "q": query, "count": num_results }
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    results = []
    for item in data.get("web", {}).get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "snippet": item.get("description")
        })

    return results

def fetch_page_text(url, max_chars=50000):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove junk
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)

        return text[:max_chars]

    except Exception as e:
        return f"[Error fetching {url}: {e}]"

def retrieve_context_by_brave(query):
    search_results = brave_search(query)

    context = ""

    for r in search_results:
        print(f"Fetching: {r['url']}")
        page_text = fetch_page_text(r["url"])

        context += f"\n\n[Source: {r['url']}]\n{page_text}"

    return context


# 2. Ask llm
def ask_llm(prompt):
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]


# 3. Main agent logic
def web_augmented_chat(question):
    print("🔎 Searching web...")
    #search_results = search_web(question)
    search_results = retrieve_context_by_brave(question)

    prompt = f"""
You are an AI assistant with access to web search results.

Use the following search results to answer the question.

Search Results:
{search_results}

Question:
{question}

Answer clearly and concisely.
"""

    print("🧠 Generating answer...\n")
    return ask_llm(prompt)


# CLI
if __name__ == "__main__":
    print(f"🌐 Web-enabled Chatbot ({MODEL} + Ollama)\n")
    print("Type 'exit' to quit\n")

    while True:
        q = input("Question: ")
        if q.lower() in ["exit", "quit"]: break

        answer = web_augmented_chat(q)
        print(f"Bot: {answer}\n")
