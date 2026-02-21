import json
import numpy as np
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "q-vercel-latency.json")

with open(DATA_PATH) as f:
    data = json.load(f)


@app.options("/api/latency")
async def options_handler():
    return {}


@app.post("/api/latency")
async def latency(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 0)

    result = {}

    for region in regions:
        rows = [r for r in data if r.get("region") == region]
        latencies = [r.get("latency_ms", 0) for r in rows]
        uptimes = [r.get("uptime", 0) for r in rows]

        if not latencies:
            result[region] = {
                "avg_latency": 0,
                "p95_latency": 0,
                "avg_uptime": 0,
                "breaches": 0,
            }
            continue

        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": sum(l > threshold for l in latencies),
        }

    return result

# import json
# import numpy as np
# import os
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load JSON safely
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_PATH = os.path.join(BASE_DIR, "..", "q-vercel-latency.json")

# try:
#     with open(DATA_PATH) as f:
#         data = json.load(f)
# except Exception as e:
#     data = []
#     print("JSON LOAD ERROR:", e)


# @app.post("/api/latency")
# async def latency(payload: dict):
#     try:
#         regions = payload.get("regions", [])
#         threshold = payload.get("threshold_ms", 0)

#         result = {}

#         for region in regions:
#             rows = [r for r in data if r.get("region") == region]
#             latencies = [r.get("latency_ms", 0) for r in rows]
#             uptimes = [r.get("uptime", 0) for r in rows]

#             if not latencies:
#                 result[region] = {
#                     "avg_latency": 0,
#                     "p95_latency": 0,
#                     "avg_uptime": 0,
#                     "breaches": 0,
#                 }
#                 continue

#             result[region] = {
#                 "avg_latency": float(np.mean(latencies)),
#                 "p95_latency": float(np.percentile(latencies, 95)),
#                 "avg_uptime": float(np.mean(uptimes)),
#                 "breaches": sum(l > threshold for l in latencies),
#             }

#         return result

#     except Exception as e:
#         return {"error": str(e)}
