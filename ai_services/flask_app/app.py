# flask_app/app.py
from flask import Flask, request, jsonify
from agents.milestone_agent import generate_milestones
from agents.verification_agent import verify_submission
from agents.pfi_agent import calculate_pfi_score
from agents.negotiation_agent import check_negotiation

app = Flask(__name__)

@app.route('/ai/generate-milestones', methods=['POST'])
def api_generate_milestones():
    data = request.json
    # Expects: project_description, budget, deadline
    result = generate_milestones(data.get('description'), data.get('budget'), data.get('deadline'))
    return jsonify(result)

@app.route('/ai/verify-milestone', methods=['POST'])
def api_verify_milestone():
    data = request.json
    # Expects: github_repository_link
    result = verify_submission(data.get('github_link'))
    return jsonify(result)

@app.route('/ai/calculate-pfi', methods=['POST'])
def api_calculate_pfi():
    data = request.json
    # Expects: completion_rate, adherence, quality_score
    result = calculate_pfi_score(data)
    return jsonify(result)

@app.route('/ai/negotiation-check', methods=['POST'])
def api_negotiation_check():
    data = request.json
    # Expects: description, budget
    result = check_negotiation(data.get('description'), data.get('budget'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
    