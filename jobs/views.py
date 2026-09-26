from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from accounts.models import Profile
from .forms import JobForm, JobSearchForm
from .models import Job

# Create your views here.

def index(request):
    jobs = Job.objects.filter(is_active=True)

    #builds the search form from string. Now if refresh happens itll save the filters
    form = JobSearchForm(request.GET or None)

    #only go in queryset when filters get validated
    if form.is_valid():
        title = form.cleaned_data.get('title')
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        min_salary = form.cleaned_data.get('min_salary')
        max_salary = form.cleaned_data.get('max_salary')
        work_mode = form.cleaned_data.get('work_mode')
        visa_sponsorship = form.cleaned_data.get('visa_sponsorship')

        #skips any fields that user left blank or it will narrow the query
        #with a contains match
        if title:
            jobs = jobs.filter(title__icontains=title)

        if skills:
            jobs = jobs.filter(skills__icontains=skills)

        if location:
            jobs = jobs.filter(location__icontains=location)

        # a jobs salary range and the filter's salary range must be inside each other.
        # so job paying $60k-$90k should match a filter of $70k-$120k.
        if min_salary is not None:
            jobs = jobs.filter(max_salary__gte=min_salary)

        if max_salary is not None:
            jobs = jobs.filter(min_salary__lte=max_salary)

        #itll be an exact match for work mode
        if work_mode:
            jobs = jobs.filter(work_mode=work_mode)

        #if it is checked itll filter sponsorship jobs
        if visa_sponsorship:
            jobs = jobs.filter(visa_sponsorship=True)

    #new jobs come first 
    jobs = jobs.order_by('-created_at')

    template_data = {}
    template_data['title'] = 'Jobs'
    template_data['jobs'] = jobs

    #pass the form back so template can re-display 
    return render(request, 'jobs/index.html', {
        'template_data': template_data,
        'form': form,
    })


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