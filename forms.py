"""
Forms for user signup.
Uses Django's built-in UserCreationForm.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Simple signup form with email field added."""
    email = forms.EmailField(required=False, help_text='Optional. Add your email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
