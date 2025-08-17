import os
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

class TriageResult(BaseModel):
    route: str
    reasoning: str

SYSTEM = """You are a triage router. Given a user query, choose one route:
- 'trend_research' if the user wants market/news/trend analysis or web-sourced insight
- 'other' if it's unrelated to trends (e.g., internal ops request).
Return JSON with keys route and reasoning. Keep route to the exact strings above.
"""

async def run_triage(query: str) -> dict:
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
        # Lightweight, no tools needed here
    )
    data = resp.output[0].content[0].text  # JSON string
    import json
    parsed = json.loads(data)
    return TriageResult(**parsed).model_dump()
