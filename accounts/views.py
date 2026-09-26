from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, JobSeekerProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404


# Create your views here.

@login_required
def logout(request):
 auth_logout(request)
 return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',{'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')



def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',{'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            Profile.objects.create(user=user, role=form.cleaned_data['role'])

            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != 'JOB_SEEKER':
        return redirect('home.index')

    template_data = {}
    template_data['title'] = 'Profile'
    template_data['profile'] = profile

    return render(
        request,
        'accounts/profile.html',
        {'template_data': template_data},
    )


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "JOB_SEEKER":
        return redirect('home.index')

    template_data = {}
    template_data['title'] = 'Edit Profile'

    if request.method == 'GET':
        form = JobSeekerProfileForm(
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'headline': profile.headline,
                'location': profile.location,
                'skills': profile.skills,
                'education': profile.education,
                'work_experience': profile.work_experience,
                'projects': profile.projects,
                'linkedin_url': profile.linkedin_url,
                'github_url': profile.github_url,
                'portfolio_url': profile.portfolio_url,
                'profile_public': profile.profile_public
            }
        )

        template_data['form'] = form

        return render(request,'accounts/edit_profile.html',{'template_data': template_data})

    elif request.method == 'POST':
        form = JobSeekerProfileForm(request.POST)

        if form.is_valid():
            request.user.first_name = (form.cleaned_data['first_name'])
            request.user.last_name = (form.cleaned_data['last_name'])
            request.user.email = (form.cleaned_data['email'])

            request.user.save()

            profile.headline = (form.cleaned_data['headline'])
            profile.location = (form.cleaned_data['location'])
            profile.skills = (form.cleaned_data['skills'])
            profile.education = (form.cleaned_data['education'])
            profile.work_experience = (form.cleaned_data['work_experience'])
            profile.projects = (form.cleaned_data['projects'])
            profile.linkedin_url = (form.cleaned_data['linkedin_url'])
            profile.github_url = (form.cleaned_data['github_url'])
            profile.portfolio_url = (form.cleaned_data['portfolio_url'])
            profile.profile_public = (form.cleaned_data['profile_public'])

            profile.save()

            return redirect('accounts.profile')

        else:
            template_data['form'] = form
            return render(request,'accounts/edit_profile.html',{'template_data': template_data})


@login_required
def profile_detail(request, id):
    profile = get_object_or_404(Profile, id=id, role="JOB_SEEKER")

    # Check the profile privacy
    if not profile.profile_public and profile.user_id != request.user.id:
        raise Http404("Profile is not public.")

    template_data = {}
    template_data['title'] = f"{profile.user.username}'s Profile"
    template_data['profile'] = profile

    return render(request, 'accounts/profile.html', {'template_data': template_data})

@login_required
def search_seekers(request):
    if request.user.profile.role != 'RECRUITER':
        return redirect('home.index')

    filters = {
        field: request.GET.get(field, '').strip()
        for field in ('skills', 'location', 'projects')
    }

    profiles = Profile.objects.filter(role='JOB_SEEKER', profile_public=True,).select_related('user')

    for field, value in filters.items():
        if value:
            profiles = profiles.filter(**{f'{field}__icontains': value})
    template_data = {
        'title': 'Search Job Seekers',
        'profiles': profiles,
        'filters': filters,
    }
    return render(request, 'accounts/search_seekers.html', {
        'template_data': template_data,
    })