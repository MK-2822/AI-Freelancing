from django.shortcuts import render
import requests
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .models import User, Project, Milestone, ProjectApplication, Submission
from .serializers import (UserSerializer, ProjectSerializer, MilestoneSerializer,
                          ProjectApplicationSerializer, SubmissionSerializer)

FLASK_AI_URL = "http://127.0.0.1:5001/ai"

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'role': user.role, 'id': user.id})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save(client=self.request.user)
        
        # 1. Trigger AI Negotiation Check
        try:
            neg_resp = requests.post(f"{FLASK_AI_URL}/negotiation-check", json={
                "description": project.description,
                "budget": str(project.budget)
            }, timeout=10)
            if neg_resp.status_code == 200:
                neg_data = neg_resp.json()
                if neg_data.get('status') == 'Unrealistic':
                    print(f"AI Warning: {neg_data.get('message')}")
        except requests.RequestException:
            pass

        # 2. Trigger Flask AI Milestone Generation
        try:
            ai_resp = requests.post(f"{FLASK_AI_URL}/generate-milestones", json={
                "project_id": project.id,
                "description": project.description,
                "budget": str(project.budget),
                "deadline": project.deadline.isoformat() if project.deadline else None
            }, timeout=10)
            
            if ai_resp.status_code == 200:
                milestones = ai_resp.json().get('milestones', [])
                for m in milestones:
                    Milestone.objects.create(
                        project=project,
                        title=m.get('title', 'AI Milestone'),
                        description=m.get('description', ''),
                        payment=m.get('payment', 0.00)
                    )
        except requests.RequestException as e:
            print(f"AI Service Error (Milestones): {e}")

class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(project_id=self.kwargs['project_id'])

class ProjectApplyView(generics.CreateAPIView):
    queryset = ProjectApplication.objects.all()
    serializer_class = ProjectApplicationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'Freelancer':
            return Response({'error': 'Only engineers can connect to project nodes.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if already applied
        project_id = request.data.get('project')
        if ProjectApplication.objects.filter(project_id=project_id, freelancer=request.user).exists():
            return Response({'error': 'Neural link already established for this node.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user)

class MilestoneSubmitView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        submission = serializer.save(freelancer=self.request.user)
        
        # Trigger Flask AI Verification
        try:
            ai_resp = requests.post(f"{FLASK_AI_URL}/verify-milestone", json={
                "github_link": submission.github_link
            }, timeout=10)

            if ai_resp.status_code == 200:
                result = ai_resp.json()
                score = result.get('quality_score', 0.0)
                is_copied = result.get('is_plagiarized', False)

                submission.quality_score = score
                submission.is_plagiarized = is_copied

                freelancer = submission.freelancer

                if is_copied:
                    submission.status = 'Rejected - Fraud Detected'
                    freelancer.pfi_score -= 20.0  # Heavy penalty
                    freelancer.save()
                elif score >= 80.0:
                    submission.status = 'Auto-Approved'

                    # Escrow logic: Deduct from client and add to freelancer
                    client = submission.milestone.project.client
                    payment_amount = submission.milestone.payment
                    
                    if client.wallet_balance >= payment_amount:
                        client.wallet_balance -= payment_amount
                        freelancer.wallet_balance += payment_amount
                        client.save()
                        freelancer.save()

                        # PFI Score badha do (Gamification)
                        freelancer.pfi_score += 5.0
                        freelancer.save()

                        # Milestone update
                        milestone = submission.milestone
                        milestone.status = 'Paid'
                        milestone.save()
                    else:
                        submission.status = 'Payment Failed - Client Insufficient Funds'
                else:
                    submission.status = 'Needs Revision'
                    freelancer.pfi_score -= 2.0
                    freelancer.save()

                submission.save()

        except requests.RequestException as e:
            print(f"AI Service Error (Verification): {e}")

# Create your views here.
class SmartMatchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        # Top 3 freelancers jinka PFI score sabse zyada hai
        top_freelancers = User.objects.filter(role='Freelancer').order_by('-pfi_score')[:3]
        data = [{"id": f.id, "username": f.username, "pfi_score": f.pfi_score} for f in top_freelancers]
        return Response({"recommended_freelancers": data})

