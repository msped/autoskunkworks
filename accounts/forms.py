from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    """Form to log a user in"""
    username = forms.CharField(label="E-mail")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['E-mail', 'Password']

class UserRegisterForm(UserCreationForm):
    """Form for registering a new user"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

    def clean_username(self):
        """Checks that username isn't already taken"""
        username = self.cleaned_data.get('username')
        if username == '':
            raise forms.ValidationError(u'Username address is required')
        elif User.objects.filter(username=username):
            raise forms.ValidationError(u'Username address must be unique')
        return username

    def clean_email(self):
        """checks if email is already in use"""
        email = self.cleaned_data.get('email')
        if email == '':
            raise forms.ValidationError(u'Email address is required')
        elif User.objects.filter(email=email):
            raise forms.ValidationError(u'Email address must be unique')
        return email

    def clean_password2(self):
        """Checks is password match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")

        if password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2
