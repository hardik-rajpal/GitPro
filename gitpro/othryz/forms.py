from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import request

class GitProUserForm(UserCreationForm):
    username=forms.CharField(max_length=150, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    first_name=forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']