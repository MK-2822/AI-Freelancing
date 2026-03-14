# flask_app/agents/pfi_agent.py

def calculate_pfi_score(data):
    # Formula: 0.4*completion + 0.3*adherence + 0.3*quality
    cr = float(data.get('completion_rate', 0))
    da = float(data.get('deadline_adherence', 0))
    qs = float(data.get('quality_score', 0))
    
    pfi = (0.4 * cr) + (0.3 * da) + (0.3 * qs)
    
    return {
        "pfi_score": float(f"{pfi:.2f}"),
        "rating": "Top Rated" if pfi > 85 else "Standard",
        "metrics_analyzed": ["completion", "adherence", "quality"]
    }