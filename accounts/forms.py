from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(choices=[('JOB_SEEKER', 'Job Seeker'), ('RECRUITER', 'Recruiter')])

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields.values():
<<<<<<< Updated upstream
            fieldname.widget.attrs.update({'class': 'form-control'})
=======
            fieldname.widget.attrs.update({'class': 'form-control'})


class JobSeekerProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    headline = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)
    skills = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5}))
    education = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    work_experience = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 10}))
    projects = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5}))
    linkedin_url = forms.URLField(required=False)
    github_url = forms.URLField(required=False)
    portfolio_url = forms.URLField(required=False)
    profile_public = forms.BooleanField(required=False, label="Make profile visible to recruiters")

    def __init__(self, *args, **kwargs):
        super(JobSeekerProfileForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields.values():
            fieldname.widget.attrs.update({'class': 'form-control'})

        self.fields['profile_public'].widget.attrs.update({'class': 'form-check-input'})



>>>>>>> Stashed changes
