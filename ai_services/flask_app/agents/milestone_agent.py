# flask_app/agents/milestone_agent.py

def generate_milestones(description, budget, deadline):
    # Mocking AI logic with keyword detection for a high-quality demo
    desc = description.lower()
    
    if "defi" in desc or "blockchain" in desc:
        workflow = [
            ("Smart Contract Architecture", 0.20),
            ("Liquidity Pool Logic & Auditing", 0.35),
            ("Web3 Provider Integration", 0.25),
            ("Mainnet Staging & Gas Optimization", 0.20)
        ]
    elif "ai" in desc or "ml" in desc or "trading" in desc:
        workflow = [
            ("Neural Data Pipeline & Cleaning", 0.25),
            ("Model Architecture & Training", 0.40),
            ("Inference API & Real-time Stream", 0.20),
            ("Optimization & Latency Stress Test", 0.15)
        ]
    else:
        workflow = [
            ("Infrastructure & Database Schema", 0.15),
            ("Core API Engine & Business Logic", 0.45),
            ("Frontend UI/UX Implementation", 0.25),
            ("Final System Integration & QA", 0.15)
        ]
    
    response = {
        "project": description,
        "total_budget": budget,
        "deadline": deadline,
        "milestones": []
    }

    for i, (title, share) in enumerate(workflow):
        response["milestones"].append({
            "step": i + 1,
            "title": title,
            "payment": round(float(budget) * share, 2),
            "status": "pending"
        })
    
    return response