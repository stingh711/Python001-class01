from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Wrong username or password")

        return cleaned_data
