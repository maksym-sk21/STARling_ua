from django import forms

class LessonPaymentForm(forms.Form):
    lesson_count = forms.IntegerField(label='Количество уроков', min_value=1)
    language = forms.ChoiceField(label='Язык', choices=[('english', 'Английский'), ('german', 'Немецкий')])
