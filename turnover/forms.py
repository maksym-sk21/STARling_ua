from django import forms
from .models import Turnover, TotalTurnover, TeacherCalculation, School, Salary, Client
from students.models import Student
from teachers.models import Teacher
from schedule.models import Lesson
from django.db import transaction
from .signals import update_related_models, update_teacher_budget

class TurnoverForm(forms.ModelForm):
    class Meta:
        model = Turnover
        fields = [
            'student',
            'teacher',
            'previous_hours',
            'previous_balance',
            'current_hours',
            'current_payment',
            'total_hours',
            'profit'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'previous_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'previous_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'profit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                with transaction.atomic():
                    update_related_models(sender=Turnover, instance=instance, created=True)
                    instance.save()

            return instance


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'turnover',
            'total_profit',
            'school_budget',
            'budget_elena',
            'budget_maria'
        ]
        widgets = {
            'turnover': forms.Select(attrs={'class': 'form-control'}),
            'total_profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'school_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_elena': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_maria': forms.NumberInput(attrs={'class': 'form-control'})
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'turnover',
            'monthly_profit',
            'monthly_budget',
            'salary_elena',
            'salary_maria'
        ]
        widgets = {
            'turnover': forms.Select(attrs={'class': 'form-control'}),
            'monthly_profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_elena': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_maria': forms.NumberInput(attrs={'class': 'form-control'})
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'turnover',
            'hourly_rate',
            'money_spent',
            'remaining_hours',
            'remaining_money'
        ]
        widgets = {
            'turnover': forms.Select(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'money_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_money': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TeacherCalculationForm(forms.ModelForm):
    class Meta:
        model = TeacherCalculation
        fields = [
            'turnover',
            'hourly_rate',
            'hours_spent',
            'salary_teacher',
            'budget_teacher'
        ]
        widgets = {
            'turnover': forms.Select(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'hours_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_teacher': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_teacher': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                print(f"Form saved: Hourly Rate: {instance.hourly_rate}")
                with transaction.atomic():
                    update_teacher_budget(sender=TeacherCalculation, instance=instance, created=True)
            return instance


class TotalTurnoverForm(forms.ModelForm):
    class Meta:
        model = TotalTurnover
        fields = [
            'total_previous_hours', 'total_previous_balance',
            'total_current_hours', 'total_current_payment',
            'total_total_hours', 'total_profit', 'total_school_budget',
            'total_budget_elena', 'total_budget_maria', 'total_monthly_profit',
            'total_monthly_budget', 'total_salary_elena', 'total_salary_maria', 'total_hours_spent',
            'total_hourly_rate', 'total_money_spent', 'total_remaining_hours',
        ]
        widgets = {
            'total_previous_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_previous_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_current_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_current_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_school_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_budget_elena': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_budget_maria': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_monthly_profit': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_monthly_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_salary_elena': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_salary_maria': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_hours_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_money_spent': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_remaining_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AssignStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Выберите студента")


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'phone_number', 'student_phone_number', 'user', 'salary']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'phone_number', 'language', 'lesson_count', 'user', 'additional_info']
