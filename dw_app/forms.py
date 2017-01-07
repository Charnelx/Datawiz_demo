import re
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())
    api_pass = forms.CharField(label='api password')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('This email is already in use.')

    def clean_api_pass(self):
        if 'api_pass' in self.cleaned_data:
            api_pass = self.cleaned_data['api_pass']
            if len(api_pass) <= 254:
                return api_pass
            raise forms.ValidationError('API password should be less or equal to 254 characters length')
        raise forms.ValidationError('You should provide your API pass')

class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        initial_start_date = kwargs.pop('initial_start_date')
        initial_end_date = kwargs.pop('initial_end_date')
        required_val = kwargs.pop('required')

        super(DateRangeForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = initial_start_date
        self.fields['start_date'].required = required_val
        self.fields['end_date'].initial = initial_end_date
        self.fields['end_date'].required = required_val