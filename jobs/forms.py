from django import forms
from .models import Job


class JobSearchForm(forms.Form):
    #case insensitive match against Job.title
    title = forms.CharField(
        required=False,
        label='Job title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    #case insensitive match against job.skills
    skills = forms.CharField(
        required=False,
        label='Skills',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    #case insensitive match against Jobs.location
    location = forms.CharField(
        required=False,
        label='Location',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    #min amount for salary range
    min_salary = forms.IntegerField(
        required=False,
        min_value=0,
        label='Min salary',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
        }),
    )
    #max range for salary range
    max_salary = forms.IntegerField(
        required=False,
        min_value=0,
        label='Max salary',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
        }),
    )
    #drop down for work type. it pulls it from the job model so cant get out of sync
    work_mode = forms.ChoiceField(
        required=False,
        label='Work mode',
        choices=[('', 'Any')] + list(Job._meta.get_field('work_mode').choices),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
    )
    #check box for sponsorship
    visa_sponsorship = forms.BooleanField(
        required=False,
        label='Visa sponsorship only',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
    )
    #Clean to help keep eveything in line such as if a user has a higher min than max
    #it will give them an error telling them why.
    def clean(self):
        cleaned_data = super().clean()

        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')

        if (
            min_salary is not None
            and max_salary is not None
            and min_salary > max_salary
            ):
                raise forms.ValidationError(
                    'The minimum salary cannot be greater than the maximum salary.'
                )

        return cleaned_data

class JobForm(forms.ModelForm):
    class Meta:
        model = Job

        fields = [
            'title',
            'description',
            'skills',
            'location',
            'min_salary',
            'max_salary',
            'work_mode',
            'visa_sponsorship',
            'is_active',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Python, Django, SQL'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'min_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'max_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'work_mode': forms.Select(attrs={
                'class': 'form-select'
            }),
            'visa_sponsorship': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
           'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')

        if (
            min_salary is not None
            and max_salary is not None
            and min_salary > max_salary
            ):
                raise forms.ValidationError(
                    'The minimum salary cannot be greater than the maximum salary.'
                )

        return cleaned_data