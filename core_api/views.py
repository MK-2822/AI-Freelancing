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

FLASK_AI_URL = "http://127.0.0.1:5000/api/ai"

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
        
        # Trigger Flask AI Milestone Generation
        try:
            ai_resp = requests.post(f"{FLASK_AI_URL}/generate-milestones", json={
                "project_id": project.id,
                "description": project.description,
                "budget": str(project.budget)
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
           if ai_resp.status_code == 200:
                result = ai_resp.json()
                score = result.get('quality_score', 0.0)
                submission.quality_score = score
                
                # MAGIC HAPPENS HERE: Auto-Approval & Payment
                if score >= 80.0:
                    submission.status = 'Auto-Approved'
                    
                    # Freelancer ko paise mil gaye!
                    freelancer = submission.freelancer
                    freelancer.wallet_balance += submission.milestone.payment
                    
                    # PFI Score badha do (Gamification)
                    freelancer.pfi_score += 5.0 
                    freelancer.save()
                    
                    # Milestone update
                    milestone = submission.milestone
                    milestone.status = 'Paid'
                    milestone.save()
                else:
                    submission.status = 'Needs Revision'
                    # Kharab code par score kam karo
                    freelancer = submission.freelancer
                    freelancer.pfi_score -= 2.0
                    freelancer.save()
                    
                submission.save()

# Create your views here.
class SmartMatchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        # Top 3 freelancers jinka PFI score sabse zyada hai
        top_freelancers = User.objects.filter(role='Freelancer').order_by('-pfi_score')[:3]
        data = [{"id": f.id, "username": f.username, "pfi_score": f.pfi_score} for f in top_freelancers]
        return Response({"recommended_freelancers": data})

is_copied = result.get('is_plagiarized', False)
                submission.is_plagiarized = is_copied
                
                if is_copied:
                    submission.status = 'Rejected - Fraud Detected'
                    freelancer.pfi_score -= 20.0 # Heavy penalty
                    freelancer.save()
