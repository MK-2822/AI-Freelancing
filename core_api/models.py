from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (('Client', 'Client'), ('Freelancer', 'Freelancer'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Freelancer')
    pfi_score = models.FloatField(default=0.0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Project(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, default='Open')

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')

class ProjectApplication(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, default='Pending')

    class Meta:
        unique_together = ('project', 'freelancer')

class Submission(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='submissions')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    github_link = models.URLField()
    notes = models.TextField(blank=True, null=True)
    quality_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Submitted')
    is_plagiarized = models.BooleanField(default=False)
# Create your models here.
