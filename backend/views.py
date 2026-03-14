from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def login_selection_view(request):
    return render(request, 'login.html')

def auth_view(request, role, mode):
    quotes = {
        'client': "TrustLancer AI found me a developer in minutes. The AI milestones are a game changer.",
        'freelancer': "I never have to worry about payment. The AI verifies my code and releases funds instantly."
    }
    return render(request, 'auth.html', {
        'role': role.capitalize(),
        'mode': mode,
        'quote': quotes.get(role.lower(), "")
    })

def client_dashboard_view(request):
    return render(request, 'client-dashboard.html', {'user_type': 'Client', 'projects': []})

def freelancer_dashboard_view(request):
    return render(request, 'freelancer-dashboard.html', {'user_type': 'Freelancer', 'projects': []})
