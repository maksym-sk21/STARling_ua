from django.db import models
from students.models import Student
from teachers.models import Teacher
from django.utils import timezone
from decimal import Decimal
# Create your models here.

class Turnover(models.Model):
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='turnovers')
    previous_hours = models.DecimalField(max_digits=10, decimal_places=2)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_hours = models.DecimalField(max_digits=10, decimal_places=2)
    current_payment = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_hours = Decimal(self.previous_hours or 0) + Decimal(self.current_hours or 0)
        self.profit = Decimal(self.previous_balance or 0) + Decimal(self.current_payment or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.teacher.name}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]


class School(models.Model):
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    school_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    budget_elena = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    budget_maria = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return f"School - {self.turnover}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]


class Salary(models.Model):
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    monthly_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    salary_elena = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    salary_maria = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return f"Salary - {self.turnover}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]


class Client(models.Model):
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    money_spent = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    remaining_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    remaining_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Client - {self.turnover}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]


class TeacherCalculation(models.Model):
    turnover = models.ForeignKey(Turnover, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    hours_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    salary_teacher = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    budget_teacher = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f"TeacherCalculation - {self.turnover}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.turnover.teacher.salary = self.salary_teacher
        self.turnover.teacher.save()


class TotalTurnover(models.Model):
    total_previous_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_previous_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_current_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_current_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_total_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_school_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_budget_elena = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_budget_maria = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_monthly_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_salary_elena = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_salary_maria = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_hours_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_money_spent = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_remaining_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salary_teacher = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_budget_teacher = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_remaining_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return f"TotalTurnover - {self.id}"

    class Meta:
        permissions = [
            ("can_view_turnover", "Can view turnover"),
            ("can_edit_turnover", "Can edit turnover"),
        ]
