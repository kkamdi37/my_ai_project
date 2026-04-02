from mcp.server.fastmcp import FastMCP
from ddgs import DDGS

mcp = FastMCP("duckduckgo")

@mcp.tool()
def search(query: str) -> str:
    """Search the web using DuckDuckGo"""
    results = []
    
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"{r['title']} - {r['href']}")

    return "\n".join(results)

if __name__ == "__main__":
    mcp.run()
