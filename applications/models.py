from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

# Create your models here.

class Application(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)

    tailored_note = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=[('APPLIED', 'Applied'), ('REVIEWED', 'Reviewed'),
                                                      ('INTERVIEWED', 'Interviewed'), ('OFFER', 'Offer'),
                                                      ('CLOSED', 'Closed')], default='APPLIED')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant.username + ' - ' + self.job.title