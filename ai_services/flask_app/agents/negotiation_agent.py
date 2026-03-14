# flask_app/agents/negotiation_agent.py

def check_negotiation(description, budget):
    # Simple complexity estimator
    complexity_keywords = ['ai', 'machine learning', 'blockchain', 'react', 'fullstack']
    estimated_min = 200
    
    for word in complexity_keywords:
        if word in description.lower():
            estimated_min += 150
            
    if budget < estimated_min:
        return {
            "status": "Unrealistic",
            "message": "Budget too low for project scope.",
            "recommended_range": f"${estimated_min} - ${estimated_min + 300}",
            "suggestion": "Increase budget to attract high-quality developers."
        }
    
    return {
        "status": "Fair",
        "message": "The budget aligns with market standards for this scope."
    }