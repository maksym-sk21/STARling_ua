from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Lesson
        fields = ['teacher', 'student', 'date', 'start_time', 'duration', 'conducted']
