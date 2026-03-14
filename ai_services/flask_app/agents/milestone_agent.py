# flask_app/agents/milestone_agent.py

def generate_milestones(description, budget, deadline):
    # In a real scenario, you'd send 'description' to OpenAI/GPT-4 here.
    # Mocking AI logic based on keywords:
    milestones = [
        {"milestone": "Project Initialization & Requirements", "share": 0.10},
        {"milestone": "Core Backend & Database Setup", "share": 0.30},
        {"milestone": "Frontend Integration & UI", "share": 0.30},
        {"milestone": "Testing & Final Deployment", "share": 0.30},
    ]
    
    response = {
        "project": description,
        "total_budget": budget,
        "deadline": deadline,
        "milestones": []
    }

    for i, m in enumerate(milestones):
        response["milestones"].append({
            "step": i + 1,
            "title": m["milestone"],
            "payment": float(budget) * m["share"],
            "status": "pending"
        })
    
    return response
    