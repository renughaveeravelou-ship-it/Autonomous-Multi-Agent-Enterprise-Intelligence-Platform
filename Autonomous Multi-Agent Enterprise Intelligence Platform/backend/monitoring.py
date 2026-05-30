# backend/monitoring.py

import random
import time

def get_telemetry_metrics():
    """Generates mock Prometheus-style performance telemetry metrics."""
    return {
        "system": {
            "cpu_utilization_pct": round(22.4 + random.uniform(-5.0, 5.0), 1),
            "memory_usage_gb": round(6.8 + random.uniform(-0.2, 0.2), 2),
            "memory_utilization_pct": round(42.5 + random.uniform(-1.0, 1.0), 1),
            "uptime_seconds": int(time.time()) % 86400,
            "api_latency_ms": round(15.2 + random.uniform(-3.0, 12.0), 1)
        },
        "agents": [
            {"id": "ceo_agent", "name": "CEO Agent", "status": "Idle", "total_runs": 128, "err_rate": 0.0},
            {"id": "finance_agent", "name": "Finance Agent", "status": "Idle", "total_runs": 450, "err_rate": 0.01},
            {"id": "hr_agent", "name": "HR Agent", "status": "Idle", "total_runs": 320, "err_rate": 0.0},
            {"id": "retail_agent", "name": "Retail Agent", "status": "Idle", "total_runs": 1024, "err_rate": 0.02},
            {"id": "support_agent", "name": "Customer Support Agent", "status": "Active", "total_runs": 2840, "err_rate": 0.03},
            {"id": "risk_agent", "name": "Risk Agent", "status": "Idle", "total_runs": 612, "err_rate": 0.01}
        ],
        "model_drift": [
            {
                "model_name": "Sales Forecaster",
                "status": "Healthy",
                "population_stability_index": 0.04,
                "threshold": 0.10,
                "last_checked": "Just now"
            },
            {
                "model_name": "Employee Attrition Predictor",
                "status": "Healthy",
                "population_stability_index": 0.08,
                "threshold": 0.10,
                "last_checked": "5 mins ago"
            },
            {
                "model_name": "Ticket Sentiment Classifier",
                "status": "Warning (Drift)",
                "population_stability_index": 0.14,
                "threshold": 0.10,
                "last_checked": "10 mins ago"
            },
            {
                "model_name": "Risk Index Volatility Predictor",
                "status": "Healthy",
                "population_stability_index": 0.02,
                "threshold": 0.10,
                "last_checked": "Just now"
            }
        ],
        "alerts": [
            {"timestamp": "16:10:45", "severity": "Info", "source": "RAG System", "message": "Indexed 15 company document descriptors successfully."},
            {"timestamp": "16:22:12", "severity": "Warning", "source": "Ticket Sentiment Classifier", "message": "Feature distribution drift detected (PSI = 0.14). Re-training recommended."},
            {"timestamp": "16:35:01", "severity": "Info", "source": "Consensus Engine", "message": "Active consensus reached between Finance Agent and Risk Agent on Q3 allocations."}
        ]
    }
