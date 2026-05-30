# backend/main.py

import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import local modules
from backend.simulation import run_what_if_simulation, load_dataset_stats
from backend.agents import generate_agent_flow
from backend.graph import get_workforce_graph, get_supply_chain_graph, get_financial_graph
from backend.rag import rag_engine
from backend.monitoring import get_telemetry_metrics

app = FastAPI(
    title="Autonomous Multi-Agent Enterprise Intelligence Platform",
    description="Unified AI intelligence dashboard powered by collaborative sub-agents.",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schemas
class ChatRequest(BaseModel):
    message: str

class SimulationRequest(BaseModel):
    headcount_change: float
    marketing_change: float
    markup_change: float
    sla_target: float
    risk_tolerance: str

# API Routes
@app.get("/api/health")
def health_check():
    return {
        "status": "running",
        "system": "Autonomous Multi-Agent Enterprise Intelligence Platform"
    }

@app.post("/api/chat")
def chat_copilot(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        flow = generate_agent_flow(req.message)
        # Integrate local document retrieval context (RAG) into chat response metadata
        retrieved_docs = rag_engine.retrieve(req.message, limit=2)
        flow["retrieved_context"] = retrieved_docs
        return flow
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
def simulate_metrics(req: SimulationRequest):
    try:
        results = run_what_if_simulation(
            headcount_change=req.headcount_change,
            marketing_change=req.marketing_change,
            markup_change=req.markup_change,
            sla_target=req.sla_target,
            risk_tolerance=req.risk_tolerance
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/graphs/{graph_type}")
def get_network_graph(graph_type: str):
    if graph_type == "workforce":
        return get_workforce_graph()
    elif graph_type == "supply_chain":
        return get_supply_chain_graph()
    elif graph_type == "financial":
        return get_financial_graph()
    else:
        raise HTTPException(status_code=400, detail="Invalid graph type. Choose: workforce, supply_chain, financial")

@app.get("/api/rag/search")
def search_documents(q: str = Query(..., min_length=2)):
    return {
        "query": q,
        "results": rag_engine.retrieve(q, limit=5)
    }

@app.get("/api/monitoring/metrics")
def get_telemetry():
    return get_telemetry_metrics()

@app.get("/api/datasets/stats")
def get_datasets():
    return load_dataset_stats()

# Mount frontend static files
# Make sure frontend folder exists
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # When run directly, start the server
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
