import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.agents.triage_agent import run_triage
from app.agents.trend_agent import run_trend_research

app = FastAPI(title="Triage & Trend Research Agents")

class TriageResponse(BaseModel):
    route: str
    reasoning: str

class TrendRequest(BaseModel):
    topic: str
    timeframe: str | None = None
    max_sources: int = 6

@app.get("/healthz")
def healthz():
    return {"ok": True, "model": os.getenv("OPENAI_MODEL", "gpt-5")}

@app.get("/triage", response_model=TriageResponse)
async def triage(q: str = Query(..., description="User query to route")):
    return await run_triage(q)

@app.post("/research")
async def research(req: TrendRequest):
    return await run_trend_research(
        topic=req.topic,
        timeframe=req.timeframe,
        max_sources=req.max_sources
    )

def run():
    # For Railway: PORT is provided
    import uvicorn, os
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8080")), reload=False)
