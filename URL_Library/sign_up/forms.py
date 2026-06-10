from django import forms
from .models import User, UserContent


class SignupForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            self.add_error("email", "Email already in use")

        if User.objects.filter(username=cleaned_data.get("username")).exists():
            self.add_error("username", "Username already in use")

        return cleaned_data
