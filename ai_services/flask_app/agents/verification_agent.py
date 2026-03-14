# flask_app/agents/verification_agent.py
import random

def verify_submission(github_link):
    if not github_link or "github.com" not in github_link:
        return {"status": "rejected", "reason": "Invalid Repository Link"}

    # Hackathon Logic: Simulate code analysis
    # Real version: Use GitHub API to check latest commits/PRs
    quality_score = random.randint(70, 95) 
    
    return {
        "completion_status": "Verified",
        "quality_score": quality_score,
        "approval_or_rejection": "Approved" if quality_score > 75 else "Needs Revision",
        "feedback": "Code follows PEP8 standards. Good documentation found."
    }