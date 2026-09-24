from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=100, choices=[('JOB_SEEKER', 'Job Seeker'), ('RECRUITER', 'Recruiter')])

    headline = models.CharField(max_length=255, blank=True)

    skills = models.TextField(blank=True)

    education = models.TextField(blank=True)

    work_experience = models.TextField(blank=True)

    projects = models.TextField(blank=True)

    location = models.TextField(blank=True)

    linkedin_url = models.URLField(blank=True)

    github_url = models.URLField(blank=True)

    portfolio_url = models.URLField(blank=True)

    profile_public = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username