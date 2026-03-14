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

from core_api.models import Project

def client_dashboard_view(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'client-dashboard.html', {'user_type': 'Client', 'projects': projects})

def freelancer_dashboard_view(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'freelancer-dashboard.html', {'user_type': 'Freelancer', 'projects': projects})

def projects_view(request):
    user_type = getattr(request.user, 'role', 'Freelancer')
    projects = Project.objects.all().order_by('-id')
    return render(request, 'projects.html', {'projects': projects, 'user_type': user_type})

def payments_view(request):
    user_type = getattr(request.user, 'role', 'Freelancer')
    return render(request, 'payments.html', {'user_type': user_type})

def agent_lab_view(request):
    user_type = getattr(request.user, 'role', 'Freelancer')
    return render(request, 'agent_lab.html', {'user_type': user_type})

def marketplace_view(request):
    user_type = getattr(request.user, 'role', 'Freelancer')
    projects = Project.objects.filter(status='Open').order_by('-id')
    return render(request, 'marketplace.html', {'projects': projects, 'user_type': user_type})
