import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core_api.models import User, Project, Milestone

def seed_data():
    print("Seed process initialized. Purging existing node data...")
    # Delete existing data to start fresh
    Project.objects.all().delete()
    Milestone.objects.all().delete()
    
    # Ensure users exist
    client, _ = User.objects.get_or_create(username='Alpha_Client', email='client@trust.ai')
    if _:
        client.set_password('pass123')
        client.role = 'Client'
        client.save()

    freelancer, _ = User.objects.get_or_create(username='Neural_Engineer', email='eng@trust.ai')
    if _:
        freelancer.set_password('pass123')
        freelancer.role = 'Freelancer'
        freelancer.pfi_score = 98.4
        freelancer.save()

    # Create Projects
    projects_data = [
        {
            'title': 'Autonomous Liquidity Protocol',
            'desc': 'Build a decentralized DeFi liquidity aggregator with AI-managed risk profiles and cross-chain bridging.',
            'budget': 15000,
            'status': 'In Progress',
            'milestones': [
                ('Smart Contract V1 - Liquidity Engine', 3000, 'Paid'),
                ('Risk Assessment AI Integration', 5000, 'Completed'),
                ('Cross-chain bridge relay nodes', 4000, 'Open'),
                ('Security Audit & Mainnet Launch', 3000, 'Open'),
            ]
        },
        {
            'title': 'Generative UI Neural Engine',
            'desc': 'Developing a system that generates React components based on natural language project visions.',
            'budget': 8000,
            'status': 'Open',
            'milestones': [
                ('LLM fine-tuning for tailwind patterns', 2000, 'Open'),
                ('Dynamic Component Renderer', 3000, 'Open'),
                ('Integration with TrustLancer API', 3000, 'Open'),
            ]
        },
        {
            'title': 'Zk-Proof Identity Gateway',
            'desc': 'Implementing zero-knowledge identity verification for high-security freelancer nodes.',
            'budget': 12000,
            'status': 'In Progress',
            'milestones': [
                ('Circuit design for Zk-Snarks', 4000, 'Paid'),
                ('On-chain verification contract', 4000, 'Open'),
                ('Frontend Credential Dashboard', 4000, 'Open'),
            ]
        }
    ]

    for p_data in projects_data:
        p = Project.objects.create(
            title=p_data['title'],
            description=p_data['desc'],
            budget=p_data['budget'],
            status=p_data['status'],
            client=client,
            deadline=datetime.now() + timedelta(days=30)
        )
        for m_title, m_pay, m_status in p_data['milestones']:
            Milestone.objects.create(
                project=p,
                title=m_title,
                payment=m_pay,
                status=m_status
            )
    
    print(f"Successfully deployed {len(projects_data)} project nodes and associated milestones.")

if __name__ == '__main__':
    seed_data()
