from langchain_core.tools import tool
import requests

@tool
def search_web(query: str) -> str:
    """
    Search the web for a query string.
    """
    try:
        url = "https://searx.oloke.xyz/search"
        params = {"q": query, "format": "json"}
        r = requests.get(url, params=params)
        print(r.text)
        results = r.json()
        print(results)
        if "results" in results:
            return "\n".join([f"{r['title']}: {r['url']}" for r in results["results"][:5]])
        return "No results"
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred"