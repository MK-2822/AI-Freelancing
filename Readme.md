# AI-Freelancing: TrustLancer AI

An intelligent freelancing platform that integrates **Django** (Core REST API) and **Flask** (AI Service) to automate project milestones, code verification, freelancer matching, and payments.

![TrustLancer](https://img.shields.io/badge/Status-Beta-success) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Django](https://img.shields.io/badge/Django-5.2-green) ![Flask](https://img.shields.io/badge/Flask-3.1-black)

---

## 🚀 Features

- **🤖 AI Milestones Generator**: Automatically drafts project milestones and budget splits based on project requirements.
- **🔍 Auto-Verification**: AI agents scan submitted GitHub repositories, review the code, and assign a quality score.
- **🎯 Smart Match**: Connects clients to top freelancers based on their Gamified **PFI (Profile Factor Index) Score**.
- **💸 Automated Escrow**: Once AI approves a milestone (score > 80%), funds are automatically released to the freelancer's wallet.
- **🎨 Glassmorphism UI**: A beautifully animated frontend portal offering separate dashboards for clients and freelancers.

---

## 🛠 Tech Stack

- **Backend / Core API**: Django + Django REST Framework 
- **AI Microservice**: Flask
- **Database**: SQLite (built-in)
- **Frontend**: HTML5, Tailwind CSS, Vanilla JS
- **HTTP Client**: Requests (for inter-service communication)

---

## 📂 Project Structure

```text
AI-Freelancing/
│
├── backend/            # Django Settings, URLs, and UI views
│   ├── templates/      # Glassmorphism HTML templates
│   └── static/         # Frontend JavaScript & CSS
│
├── core_api/           # Django REST App (Models, Serializers, Views)
│   ├── models.py       # User, Project, Milestone, Submission
│   ├── views.py        # Logic for escrow, match, and AI triggering
│   └── serializers.py  # DRF Data transformation
│
├── ai_services/
│   └── flask_app/      # Flask AI Microservice
│       ├── app.py      # Flask routes (port 5001)
│       └── agents/     # Milestone, Negotiation, PFI, Verification AI logic
│
└── manage.py           # Django execution script
```

---

## 💻 How to Run (Local Development)

Because this platform uses a microservice architecture, you must run **both** servers simultaneously.

### 1. Setup the Environment
```powershell
# Activate the virtual environment
.\venv\Scripts\activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run database migrations
python manage.py migrate
```

### 2. Start the Django Server (Terminal 1)
Serves the core API (port 8000) and the visual frontend.
```powershell
.\venv\Scripts\activate
python manage.py runserver
```

### 3. Start the Flask AI Server (Terminal 2)
Handles background AI logic (port 5001).
```powershell
.\venv\Scripts\activate
cd ai_services\flask_app
python app.py
```

---

## 🌐 Navigating the Platform

Once both servers are running, open your browser:

- **Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Role Selection**: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### API Endpoints (For Testing)
- `POST /api/register`
- `POST /api/login`
- `POST /api/projects` *(Triggers Flask AI Milestone Generation)*
- `GET /api/milestones/<id>`
- `GET /api/projects/<id>/match` *(Smart Match)*
- `POST /api/milestone/submit` *(Triggers Flask Verification + Auto Escrow payment)*

---

## 📜 License

MIT License. Open-sourced for the community.