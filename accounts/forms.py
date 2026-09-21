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
            fieldname.widget.attrs.update({'class': 'form-control'})