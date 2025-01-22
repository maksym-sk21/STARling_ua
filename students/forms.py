from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'phone_number', 'language']
        labels = {
            'name': 'Імʼя',
            'surname': 'Прізвище',
            'phone_number': 'Номер телефону',
            'language': 'Мова',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }
