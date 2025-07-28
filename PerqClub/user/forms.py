from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the form is bound to POST data and if 'is_cafe' is checked
        if self.data.get('is_cafe') == 'on':
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                return cleaned_data
            else:
                self.add_error('password', "Invalid username or password")
        else:
            self.add_error('username', "Please enter both username and password")

   
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser  # If you're using a custom profile model
from django.contrib.auth.forms import PasswordChangeForm

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
