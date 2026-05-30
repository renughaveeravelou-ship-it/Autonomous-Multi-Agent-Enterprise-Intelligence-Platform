# backend/agents.py

import re
import time
import random

def classify_intent(query: str) -> str:
    """Classifies user queries into specific domain intents."""
    query_lower = query.lower()
    
    if any(w in query_lower for w in ["finance", "profit", "revenue", "margin", "money", "investment", "budget"]):
        return "Finance"
    elif any(w in query_lower for w in ["hr", "employee", "attrition", "hire", "promotion", "workforce", "staff", "headcount"]):
        return "HR"
    elif any(w in query_lower for w in ["customer", "support", "ticket", "sentiment", "escalation", "satisfaction", "csat", "sla"]):
        return "Customer Support"
    elif any(w in query_lower for w in ["retail", "sales", "inventory", "stock", "demand", "store", "walmart"]):
        return "Retail"
    elif any(w in query_lower for w in ["risk", "safety", "unemployment", "cpi", "volatility", "bear", "bull"]):
        return "Risk"
    else:
        return "CEO/General"

def generate_agent_flow(query: str):
    """
    Simulates the agent coordination execution flow for a query.
    Returns:
      - intent: classified category
      - flow_steps: list of steps representing execution trace
      - xai_data: LIME/SHAP feature weights
      - answer: synthesized text response
    """
    intent = classify_intent(query)
    
    # Custom outputs based on categorized intent
    if intent == "Finance":
        involved_agents = ["Finance Agent", "Risk Agent", "CEO Agent"]
        xai_features = ["Interest Rate", "Marketing Spend", "Operational Efficiency", "Inflation (CPI)", "Unemployment Rate"]
        xai_weights = [0.38, 0.24, 0.18, -0.12, -0.08]
        
        answer = (
            "### Executive Financial Summary\n\n"
            "The **Finance Agent** has analyzed the current investment portfolio alongside the **Risk Agent's** volatility reports. "
            "Our projected Net Profit Margin sits at **15.2%** under normal conditions. "
            "To maximize performance, the Consensus Engine recommends reallocation from low-yield bonds to high-efficiency operations, "
            "which could yield an additional **2.1%** profit margin increase. "
            "However, if inflation (CPI) exceeds 8.2%, the **Risk Agent** forecasts a volatility increase of **14%**, suggesting a defensive hedge."
        )
    elif intent == "HR":
        involved_agents = ["HR Agent", "Finance Agent", "CEO Agent"]
        xai_features = ["Average Training Score", "KPIs Met >80%", "Length of Service", "Awards Won", "Age Group"]
        xai_weights = [0.45, 0.32, 0.12, 0.08, 0.03]
        
        answer = (
            "### Strategic Workforce Insights\n\n"
            "The **HR Intelligence Agent** has simulated employee promotion probability and attrition risks using local model baselines. "
            "Our key findings suggest:\n"
            "1. **Promotion Predictor**: Employees meeting over 80% of their KPIs with an average training score > 72 demonstrate a **78%** likelihood of promotion.\n"
            "2. **Attrition Risk**: Staff attrition risk has risen to **12.4%**, particularly in departments facing budget contractions. "
            "The **Finance Agent** advises adjusting training budgets upward by **5%** to offset skill gap losses, which is projected to reduce attrition by **2.2%**."
        )
    elif intent == "Customer Support":
        involved_agents = ["Customer Support Agent", "HR Agent", "CEO Agent"]
        xai_features = ["Resolution Time Target", "Staffing Ratio", "Sentiment score (BERT)", "Channel Congestion", "Customer Lifetime Value"]
        xai_weights = [-0.41, 0.28, 0.22, -0.09, 0.05]
        
        answer = (
            "### Customer Service Optimization Blueprint\n\n"
            "The **Customer Support Agent** classified recent ticket sentiment as **68% Positive, 20% Neutral, and 12% Negative**. "
            "The escalation predictor identified that response times exceeding **4.0 hours** lead to a exponential **18%** drop in CSAT. "
            "Under the consensus agreement, we propose maintaining an active agent ratio of 1 support rep per 150 daily tickets, "
            "which guarantees a average response time of **2.5 hours** and elevates projected CSAT to **4.45 / 5.0**."
        )
    elif intent == "Retail":
        involved_agents = ["Retail Agent", "Forecasting Agent", "CEO Agent"]
        xai_features = ["Fuel Price Index", "Temperature Modifier", "Holiday Flag", "CPI Trend", "Unemployment Impact"]
        xai_weights = [-0.15, 0.21, 0.42, 0.18, -0.04]
        
        answer = (
            "### Retail & Store Sales Forecast\n\n"
            "Based on the **Walmart Sales Dataset** analysis (6,435 stores tracking history), "
            "weekly sales average **$1,046,964** per store. "
            "The **Forecasting Agent** reports that:\n"
            "- **Holiday Flags** increase weekly sales by an average of **$124,500**.\n"
            "- A 1-unit increase in standardized temperature positively correlates with food/beverage retail volume by **4.2%**.\n"
            "- Dynamic inventory reordering has been triggered to maintain **98.2%** product availability ahead of the upcoming holiday weekend."
        )
    elif intent == "Risk":
        involved_agents = ["Risk Agent", "Finance Agent", "CEO Agent"]
        xai_features = ["CPI Level", "Unemployment Rate", "Fuel Price Volatility", "Dynamic Debt Ratio", "Geopolitical Stress Factor"]
        xai_weights = [-0.34, -0.28, 0.21, 0.12, 0.05]
        
        answer = (
            "### Enterprise Risk Dashboard Summary\n\n"
            "The **Risk Agent** evaluated current systemic risk signals. "
            "The volatility forecast models indicate a **Medium Risk** environment (Score: **38.4 / 100**). "
            "Unemployment trends show a stabilizing pattern around **7.9%**, but rising Fuel Prices threaten logistics margins. "
            "We recommend implementing fuel-hedging contracts and tightening operational credit lines by **8%** to protect liquid reserves."
        )
    else:
        involved_agents = ["CEO Agent", "AI Copilot", "All Sub-agents"]
        xai_features = ["Market Dynamics", "Operations Capital", "Employee Attrition", "Customer Trust", "Regulatory Risk"]
        xai_weights = [0.25, 0.20, 0.18, 0.22, 0.15]
        
        answer = (
            "### Enterprise Multi-Agent Strategic Briefing\n\n"
            "Welcome to the **Autonomous Multi-Agent Enterprise Intelligence Platform**.\n"
            "Our corporate network is fully synchronized. "
            "All sub-agents (CEO, Finance, HR, Retail, Support, Risk) are currently **Active & Online**.\n"
            "You can direct queries to specific domains (e.g. HR planning, retail demand, portfolio risk) or adjust parameters in the 'What-If Simulation' "
            "to observe live predictions computed across our enterprise model graphs."
        )

    # Compile the steps representing logs
    flow_steps = [
        {"agent": "AI Copilot", "message": "Analyzing query syntax and structure..."},
        {"agent": "AI Copilot", f"message": f"Detected query intent as: [{intent}]. Routing execution..."},
    ]
    
    for agent in involved_agents[:-1]:
        flow_steps.append({"agent": agent, "message": f"Processing sub-domain datasets and invoking specialized ML models..."})
        flow_steps.append({"agent": agent, "message": f"Generated strategic metrics and predictions. Submitting to consensus engine..."})
        
    flow_steps.extend([
        {"agent": "Consensus Engine", "message": "Evaluating parameters. Resolving data alignment and conflict constraints..."},
        {"agent": "Consensus Engine", "message": "Consensus reached. Formatting results for CEO review..."},
        {"agent": "CEO Agent", "message": "Synthesizing executive summary and strategic planner recommendations..."},
        {"agent": "CEO Agent", "message": "Response compilation complete."}
    ])
    
    return {
        "intent": intent,
        "flow_steps": flow_steps,
        "xai": {
            "features": xai_features,
            "weights": xai_weights
        },
        "answer": answer
    }
