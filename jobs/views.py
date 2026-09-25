from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from accounts.models import Profile
from .forms import JobForm
from .models import Job

# Create your views here.

def index(request):
    jobs = Job.objects.filter(is_active=True)

    template_data = {}
    template_data['title'] = 'Jobs'
    template_data['jobs'] = jobs

    return render(request, 'jobs/index.html', {'template_data': template_data})


def require_recruiter(request):
    is_recruiter = Profile.objects.filter(
        user = request.user,
        role = 'RECRUITER',
    ).exists()

    if not is_recruiter:
        raise PermissionDenied("Only recruiters can manage job posts.")

@login_required
def my_jobs(request):
    require_recruiter(request)

    jobs = Job.objects.filter(
        recruiter=request.user,
    ).order_by('-created_at')

    return render(request, 'jobs/my_jobs.html', {
        'template_data': {'title': 'My Job Posts'},
        'jobs': jobs,
    })

@login_required
def create_job(request):
    require_recruiter(request)

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('jobs.mine')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {
        'template_data': {'title': 'Post a Job'},
        'page_title': 'Post a Job',
        'form': form,
    })

@login_required
def edit_job(request, job_id):
    require_recruiter(request)

    job = get_object_or_404(
        Job,
        pk=job_id,
        recruiter=request.user,
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs.mine')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {
        'template_data': {'title': 'Edit Job'},
        'page_title': 'Edit Job',
        'form': form,
    })