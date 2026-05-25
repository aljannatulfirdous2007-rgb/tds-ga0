from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paste the telemetry data here after downloading
TELEMETRY = {
    "amer": [{"latency_ms": 120, "uptime": 0.99}],
    "apac": [{"latency_ms": 200, "uptime": 0.95}],
}

class Request(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/api")
def analytics(req: Request):
    result = {}
    for region in req.regions:
        records = TELEMETRY.get(region, [])
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": sum(1 for l in latencies if l > req.threshold_ms)
        }
    return result
