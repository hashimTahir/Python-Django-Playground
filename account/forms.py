from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required, Enter a valid email address')

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")
