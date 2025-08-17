import os, json
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

RESEARCH_SYSTEM = """You are a trend-research analyst.
- Use the web search tool to find diverse, recent, reputable sources.
- Extract concrete facts (dates, metrics, names) and note the publish date.
- Cluster findings into themes; highlight contradictions; add a confidence rating.
- Output JSON with fields: query, timeframe, sources[{title,url,published,excerpt}], insights[{theme,summary,basis}], risks, open_questions.
"""

async def run_trend_research(topic: str, timeframe: str | None, max_sources: int = 6) -> dict:
    # Tool: OpenAI web search (built-in tool via Responses API)
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": RESEARCH_SYSTEM},
            {"role": "user", "content": f"Topic: {topic}\nTimeframe: {timeframe or 'last 90 days'}\nMax sources: {max_sources}"}
        ],
        tools=[{"type": "web_search"}],  # OpenAI web search tool
        tool_choice="auto",
        response_format={"type": "json_object"},
    )
    # Responses API returns structured output for tools + final JSON
    out = resp.output[0].content[0].text
    data = json.loads(out)
    # Add server-side metadata
    data["_generated_at"] = datetime.utcnow().isoformat() + "Z"
    data["_model"] = MODEL
    return data
