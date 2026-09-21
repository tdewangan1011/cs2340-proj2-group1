from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()

    skills = models.TextField(blank=True)

    location = models.CharField(max_length=255, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    min_salary = models.IntegerField(null=True, blank=True)

    max_salary = models.IntegerField(null=True, blank=True)

    work_mode = models.CharField(max_length=20, choices=[('REMOTE', 'Remote'), ('ONSITE', 'Onsite'), ('HYBRID', 'Hybrid')])

    visa_sponsorship = models.BooleanField(default=False)

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title