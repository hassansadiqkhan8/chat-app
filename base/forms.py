from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2", "avatar"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "username", "email", "bio"]