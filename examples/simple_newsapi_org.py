#!/bin/env python3
#
# source ~/source_me
#

import os
import requests

# Replace with your NewsAPI key (get it from https://newsapi.org)
API_KEY = os.environ['MY_NEWSAPI_APIKEY']
# Replace with the desired source (e.g., "source=bbc-news", "source=techcrunch")
FILTER = "q=apple"
#FILTER = "sources=bbc-news&category=technology"
#FILTER = "country=us&category=business"
# Number of articles to fetch
ARTICLE_COUNT = 10

# Construct the API URL
url = f"https://newsapi.org/v2/top-headlines?{FILTER}&apiKey={API_KEY}"

# Make the request
response = requests.get(url)

# Check for errors
if response.status_code != 200:
    print(f"Error fetching news: {response.status_code}")
    print(response.text)
else:
    # Parse the JSON response
    news_data = response.json()

    # Extract and print the latest articles
    print(f"Latest {ARTICLE_COUNT} news from {FILTER}:")
    for i, article in enumerate(news_data["articles"][:ARTICLE_COUNT]):
        print(f"\n{i+1}. {article['title']}")
        print(article["description"])
        print(f"Source: {article['url']}\n")
