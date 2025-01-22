from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Учень'),
        ('teacher', 'Викладач'),
    )

    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
