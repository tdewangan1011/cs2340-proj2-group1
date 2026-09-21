from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Application

# Create your views here.

@login_required
def index(request):
    applications = Application.objects.filter(applicant=request.user)

    template_data = {}
    template_data['title'] = 'My Applications'
    template_data['applications'] = applications

    return render(request, 'applications/index.html', {'template_data': template_data})