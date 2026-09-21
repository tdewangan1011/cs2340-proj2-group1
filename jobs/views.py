from django.shortcuts import render
from .models import Job

# Create your views here.

def index(request):
    jobs = Job.objects.filter(is_active=True)

    template_data = {}
    template_data['title'] = 'Jobs'
    template_data['jobs'] = jobs

    return render(request, 'jobs/index.html', {'template_data': template_data})