from django import forms
from .models import Teacher, Material


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MaterialUploadForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['file']
