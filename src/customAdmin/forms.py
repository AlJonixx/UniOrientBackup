from django import forms
from django.contrib.auth import authenticate
from django.forms import fields
from django.forms.widgets import PasswordInput
from customAdmin.models import NewUser


class AccountAuthenticationForm(forms.ModelForm):

    class Meta:
        model = NewUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid Login')
