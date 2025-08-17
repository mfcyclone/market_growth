import os, httpx

BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_KEY = os.getenv("BING_SUBSCRIPTION_KEY")

async def bing_search(q: str, count: int = 10):
    headers = {"Ocp-Apim-Subscription-Key": BING_KEY}
    params = {"q": q, "count": count, "safeSearch": "Moderate", "textDecorations": False}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(BING_ENDPOINT, headers=headers, params=params)
        r.raise_for_status()
        j = r.json()
        results = []
        for item in j.get("webPages", {}).get("value", []):
            results.append({
                "name": item.get("name"),
                "url": item.get("url"),
                "snippet": item.get("snippet"),
                "dateLastCrawled": item.get("dateLastCrawled")
            })
        return results
