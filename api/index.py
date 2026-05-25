from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TELEMETRY = [{"region":"apac","latency_ms":192.23,"uptime_pct":97.334},{"region":"apac","latency_ms":136.73,"uptime_pct":98.984},{"region":"apac","latency_ms":189.4,"uptime_pct":98.112},{"region":"apac","latency_ms":159.81,"uptime_pct":98.232},{"region":"apac","latency_ms":211.86,"uptime_pct":97.397},{"region":"apac","latency_ms":224.93,"uptime_pct":97.918},{"region":"apac","latency_ms":174.63,"uptime_pct":98.614},{"region":"apac","latency_ms":140.11,"uptime_pct":97.935},{"region":"apac","latency_ms":235.1,"uptime_pct":98.878},{"region":"apac","latency_ms":227.21,"uptime_pct":99.074},{"region":"apac","latency_ms":235.44,"uptime_pct":99.297},{"region":"apac","latency_ms":174.75,"uptime_pct":98.365},{"region":"amer","latency_ms":115.23,"uptime_pct":97.574},{"region":"amer","latency_ms":119.26,"uptime_pct":98.438},{"region":"amer","latency_ms":187.56,"uptime_pct":97.378},{"region":"amer","latency_ms":181.13,"uptime_pct":97.429},{"region":"amer","latency_ms":190.5,"uptime_pct":97.43},{"region":"amer","latency_ms":166.08,"uptime_pct":99.448},{"region":"amer","latency_ms":213.72,"uptime_pct":97.293},{"region":"amer","latency_ms":130.74,"uptime_pct":97.939},{"region":"amer","latency_ms":140.44,"uptime_pct":97.555},{"region":"amer","latency_ms":175.56,"uptime_pct":97.979},{"region":"amer","latency_ms":130.9,"uptime_pct":99.31},{"region":"amer","latency_ms":212.03,"uptime_pct":98.311}]

class Request(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/api/latency")
def analytics(req: Request):
    result = {}
    for region in req.regions:
        records = [r for r in TELEMETRY if r["region"] == region]
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > req.threshold_ms))
        }
    return result
