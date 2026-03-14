from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('selection'))

# Step 1: The Split Screen Selection
@app.route('/login')
def selection():
    return render_template('login.html')

# Step 2: The Glassmorphism Auth (Login & Register)
@app.route('/auth/<role>/<mode>')
def auth(role, mode):
    quotes = {
        'client': "TrustLancer AI found me a developer in minutes. The AI milestones are a game changer.",
        'freelancer': "I never have to worry about payment. The AI verifies my code and releases funds instantly."
    }
    return render_template('auth.html', 
                           role=role.capitalize(), 
                           mode=mode, 
                           quote=quotes.get(role.lower(), ""))

@app.route('/client-dashboard')
def client_dashboard():
    return render_template('client-dashboard.html', user_type="Client")

@app.route('/freelancer-dashboard')
def freelancer_dashboard():
    return render_template('freelancer-dashboard.html', user_type="Freelancer")

if __name__ == '__main__':
    app.run(debug=True, port=5000)