# backend/graph.py

def get_workforce_graph():
    """Returns nodes and links representing corporate collaboration structure."""
    nodes = [
        {"id": "CEO", "label": "Executive CEO Agent", "group": "Leadership", "size": 25},
        {"id": "Finance_Mgr", "label": "Finance Specialist Agent", "group": "Finance", "size": 18},
        {"id": "HR_Mgr", "label": "HR Intelligence Agent", "group": "HR", "size": 18},
        {"id": "Support_Mgr", "label": "Customer Support Agent", "group": "Support", "size": 18},
        {"id": "Retail_Mgr", "label": "Retail Optimizer Agent", "group": "Retail", "size": 18},
        {"id": "Risk_Mgr", "label": "Risk Evaluator Agent", "group": "Risk", "size": 18},
        
        {"id": "Analyst_1", "label": "Portfolio Forecaster", "group": "Finance", "size": 12},
        {"id": "Analyst_2", "label": "Workforce Planner", "group": "HR", "size": 12},
        {"id": "Analyst_3", "label": "Sentiment Tracker", "group": "Support", "size": 12},
        {"id": "Analyst_4", "label": "Inventory Planner", "group": "Retail", "size": 12},
        {"id": "Analyst_5", "label": "Volatility Predictor", "group": "Risk", "size": 12},
    ]
    
    links = [
        {"source": "CEO", "target": "Finance_Mgr", "value": 5},
        {"source": "CEO", "target": "HR_Mgr", "value": 5},
        {"source": "CEO", "target": "Support_Mgr", "value": 5},
        {"source": "CEO", "target": "Retail_Mgr", "value": 5},
        {"source": "CEO", "target": "Risk_Mgr", "value": 5},
        
        {"source": "Finance_Mgr", "target": "Analyst_1", "value": 3},
        {"source": "HR_Mgr", "target": "Analyst_2", "value": 3},
        {"source": "Support_Mgr", "target": "Analyst_3", "value": 3},
        {"source": "Retail_Mgr", "target": "Analyst_4", "value": 3},
        {"source": "Risk_Mgr", "target": "Analyst_5", "value": 3},
        
        {"source": "Finance_Mgr", "target": "Risk_Mgr", "value": 4},
        {"source": "Retail_Mgr", "target": "Support_Mgr", "value": 3},
        {"source": "HR_Mgr", "target": "Finance_Mgr", "value": 2},
    ]
    return {"nodes": nodes, "links": links}

def get_supply_chain_graph():
    """Returns nodes and links representing logistics network."""
    nodes = [
        {"id": "DC_Central", "label": "Central Distribution Center", "group": "DC", "size": 25},
        {"id": "Hub_North", "label": "Northern Logistics Hub", "group": "Hub", "size": 18},
        {"id": "Hub_South", "label": "Southern Logistics Hub", "group": "Hub", "size": 18},
        
        {"id": "Store_1", "label": "Retail Store 1 (Walmart)", "group": "Store", "size": 12},
        {"id": "Store_2", "label": "Retail Store 2 (Walmart)", "group": "Store", "size": 12},
        {"id": "Store_3", "label": "Retail Store 3 (Walmart)", "group": "Store", "size": 12},
        {"id": "Store_4", "label": "Retail Store 4 (Walmart)", "group": "Store", "size": 12},
    ]
    
    links = [
        {"source": "DC_Central", "target": "Hub_North", "value": 8},
        {"source": "DC_Central", "target": "Hub_South", "value": 8},
        
        {"source": "Hub_North", "target": "Store_1", "value": 4},
        {"source": "Hub_North", "target": "Store_2", "value": 4},
        {"source": "Hub_South", "target": "Store_3", "value": 4},
        {"source": "Hub_South", "target": "Store_4", "value": 4},
        
        {"source": "Store_1", "target": "Store_2", "value": 1},
        {"source": "Store_3", "target": "Store_4", "value": 1},
    ]
    return {"nodes": nodes, "links": links}

def get_financial_graph():
    """Returns nodes and links representing dynamic financial metrics and opex streams."""
    nodes = [
        {"id": "Equity", "label": "Capital Investment", "group": "Inflow", "size": 20},
        {"id": "Revenue", "label": "Weekly Sales Income", "group": "Inflow", "size": 25},
        {"id": "Treasury", "label": "Cash Reserve Pool", "group": "Reserve", "size": 22},
        
        {"id": "OPEX", "label": "Operational Expenditures", "group": "Outflow", "size": 18},
        {"id": "Marketing", "label": "Marketing Spend", "group": "Outflow", "size": 14},
        {"id": "Salaries", "label": "Payroll & HR", "group": "Outflow", "size": 14},
        {"id": "R_D", "label": "Research & Technology", "group": "Outflow", "size": 14},
    ]
    
    links = [
        {"source": "Equity", "target": "Treasury", "value": 5},
        {"source": "Revenue", "target": "Treasury", "value": 8},
        
        {"source": "Treasury", "target": "OPEX", "value": 6},
        {"source": "OPEX", "target": "Marketing", "value": 3},
        {"source": "OPEX", "target": "Salaries", "value": 4},
        {"source": "OPEX", "target": "R_D", "value": 3},
    ]
    return {"nodes": nodes, "links": links}
