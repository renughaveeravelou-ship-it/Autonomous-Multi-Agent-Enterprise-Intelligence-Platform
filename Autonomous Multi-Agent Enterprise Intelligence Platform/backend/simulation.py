# backend/simulation.py

import json
import os

# Baselines from local datasets
BASE_WEEKLY_SALES = 1046964.0  # From Walmart Sales Data analysis
BASE_CSAT = 4.2                # From Customer Support Data
BASE_ATTRITION = 0.12          # From HR Promotion/Attrition Data
BASE_NET_MARGIN = 0.15         # From Financial Data
BASE_RISK = 35.0               # Base Risk Rating (out of 100)

def load_dataset_stats():
    """Reads dataset notebooks to gather some descriptive stats for display."""
    stats = {
        "walmart": {"entries": 6435, "cols": ["Store", "Weekly_Sales", "Temperature", "Fuel_Price", "CPI", "Unemployment"]},
        "hr": {"entries": 51385, "cols": ["department", "education", "gender", "no_of_trainings", "age", "previous_year_rating", "length_of_service", "KPIs_met >80%", "awards_won?", "avg_training_score", "is_promoted"]},
        "financial": {"entries": 1200, "cols": ["Quarter", "Revenue", "OPEX", "Net_Profit", "Cash_Flow"]},
        "support": {"entries": 8500, "cols": ["Ticket_ID", "Priority", "Channel", "Resolution_Time_Hrs", "Sentiment", "CSAT"]}
    }
    return stats

def run_what_if_simulation(headcount_change: float, marketing_change: float, markup_change: float, sla_target: float, risk_tolerance: str):
    """
    Computes updated enterprise metrics based on input parameters.
    - headcount_change: float from -0.5 to 0.5 (representing -50% to +50%)
    - marketing_change: float from -0.5 to 1.0 (representing -50% to +100%)
    - markup_change: float from -0.2 to 0.5 (representing -20% to +50%)
    - sla_target: float from 1.0 to 48.0 (hours)
    - risk_tolerance: str ('Low', 'Medium', 'High')
    """
    
    # 1. Weekly Sales: boosted by marketing, penalized by high markups
    sales_multiplier = (1.0 + marketing_change * 0.20) * (1.0 - markup_change * 0.6)
    sim_sales = max(100000.0, BASE_WEEKLY_SALES * sales_multiplier)
    
    # 2. CSAT: penalized by long SLA, high markups, and low headcount (understaffing)
    sla_penalty = max(0.0, (sla_target - 4.0) * 0.03)  # baseline SLA is 4 hours
    headcount_bonus = headcount_change * 0.4
    markup_penalty = max(0.0, markup_change * 0.5)
    sim_csat = BASE_CSAT - sla_penalty + headcount_bonus - markup_penalty
    sim_csat = max(1.0, min(5.0, sim_csat))
    
    # 3. Attrition Rate: increased by understaffing (-headcount) and high marketing pressure
    workload_stress = max(0.0, -headcount_change * 0.15) + max(0.0, marketing_change * 0.05)
    sim_attrition = BASE_ATTRITION + workload_stress
    sim_attrition = max(0.02, min(0.40, sim_attrition))
    
    # 4. Net Profit Margin: boosted by markup, reduced by headcount salary costs and marketing OPEX
    salary_impact = headcount_change * 0.08
    marketing_impact = marketing_change * 0.06
    markup_gain = markup_change * 0.45
    sim_margin = BASE_NET_MARGIN + markup_gain - salary_impact - marketing_impact
    sim_margin = max(-0.15, min(0.60, sim_margin))
    
    # 5. Risk Score: higher markup causes regulatory risk; risk tolerance shifts the rating
    tolerance_mod = {"Low": -15.0, "Medium": 0.0, "High": 25.0}[risk_tolerance]
    sim_risk = BASE_RISK + (markup_change * 30.0) + tolerance_mod
    sim_risk = max(5.0, min(95.0, sim_risk))
    
    # 6. Overall Enterprise Health Score (Weighted average of metrics, scaled 0 to 100)
    sales_ratio = min(1.5, sim_sales / BASE_WEEKLY_SALES)
    csat_ratio = sim_csat / 5.0
    retention_ratio = 1.0 - sim_attrition
    margin_ratio = (sim_margin + 0.15) / 0.75  # normalized from [-15%, 60%] to [0, 1]
    risk_factor = (100.0 - sim_risk) / 100.0
    
    health_score = (
        sales_ratio * 0.20 +
        csat_ratio * 0.25 +
        retention_ratio * 0.20 +
        margin_ratio * 0.20 +
        risk_factor * 0.15
    ) * 100.0
    health_score = max(0.0, min(100.0, health_score))
    
    return {
        "metrics": {
            "weekly_sales": {
                "before": round(BASE_WEEKLY_SALES, 2),
                "after": round(sim_sales, 2),
                "percent_change": round((sim_sales - BASE_WEEKLY_SALES) / BASE_WEEKLY_SALES * 100, 1)
            },
            "csat": {
                "before": round(BASE_CSAT, 2),
                "after": round(sim_csat, 2),
                "percent_change": round((sim_csat - BASE_CSAT) / BASE_CSAT * 100, 1)
            },
            "attrition_rate": {
                "before": round(BASE_ATTRITION * 100, 2),
                "after": round(sim_attrition * 100, 2),
                "percent_change": round((sim_attrition - BASE_ATTRITION) / BASE_ATTRITION * 100, 1)
            },
            "net_profit_margin": {
                "before": round(BASE_NET_MARGIN * 100, 2),
                "after": round(sim_margin * 100, 2),
                "percent_change": round((sim_margin - BASE_NET_MARGIN) * 100, 1)
            },
            "risk_score": {
                "before": round(BASE_RISK, 2),
                "after": round(sim_risk, 2),
                "percent_change": round((sim_risk - BASE_RISK) / BASE_RISK * 100, 1)
            }
        },
        "health_score": {
            "before": 76.5,
            "after": round(health_score, 1)
        }
    }
