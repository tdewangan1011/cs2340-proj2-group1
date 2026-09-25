from django import forms
from .models import Job

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