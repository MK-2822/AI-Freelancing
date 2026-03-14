from django.urls import path
from .views import (RegisterView, LoginView, ProjectListCreateView, 
                    MilestoneListView, ProjectApplyView, MilestoneSubmitView, SmartMatchView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('projects/', ProjectListCreateView.as_view(), name='projects'),
    path('milestones/<int:project_id>/', MilestoneListView.as_view(), name='milestones'),
    path('project/apply/', ProjectApplyView.as_view(), name='project-apply'),
    path('milestone/submit/', MilestoneSubmitView.as_view(), name='milestone-submit'),
    path('projects/<int:project_id>/match/', SmartMatchView.as_view(), name='smart-match'),
]