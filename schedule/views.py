from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Lesson
from students.models import Student
from teachers.models import Teacher
from turnover.models import Client, TeacherCalculation, Turnover, Salary
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime
from django.utils import timezone
import os


@login_required
def mark_lesson_conducted(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, teacher=request.user.teacher)

    if not lesson.conducted:
        lesson.conducted = True
        lesson.save()

        student = lesson.student
        teacher = lesson.teacher

        turnover = get_object_or_404(Turnover, student=student, teacher=teacher)

        client = get_object_or_404(Client, turnover=turnover)

        duration = lesson.duration

        if client.remaining_hours > 0:
            client.remaining_hours -= duration
            client.money_spent += client.hourly_rate * duration
            client.remaining_money -= client.hourly_rate * duration
            client.save()

        teacher_calculation = get_object_or_404(TeacherCalculation, turnover=turnover)
        teacher_calculation.hours_spent += duration
        teacher_calculation.salary_teacher += teacher_calculation.hourly_rate * duration
        teacher_calculation.save()

        salary, created = Salary.objects.get_or_create(turnover=turnover)
        monthly_profit = client.money_spent - teacher_calculation.salary_teacher
        salary.monthly_profit = monthly_profit
        salary.monthly_budget = monthly_profit * Decimal('0.30')
        salary.salary_elena = monthly_profit * Decimal('0.40')
        salary.salary_maria = monthly_profit * Decimal('0.30')
        salary.save()

    return redirect('teachers:teacher_area')


@login_required
def schedule_view(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    lessons = Lesson.objects.filter(teacher=teacher).order_by('date', 'start_time')

    return render(request, 'schedule/schedule.html', {'lessons': lessons})


@login_required
def add_lesson(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = request.POST.get('duration')
        student_id = request.POST.get('student_id')

        if date and start_time and duration and student_id:
            start_time = datetime.strptime(f'{date} {start_time}', '%Y-%m-%d %H:%M')

            student = get_object_or_404(Student, id=student_id)

            Lesson.objects.create(
                date=date,
                start_time=start_time,
                duration=Decimal(duration),
                teacher=request.user.teacher,
                student=student,
            )

            return redirect('schedule:schedule_view')

    return render(request, 'schedule/add_lesson.html')


@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, teacher=request.user.teacher)

    if request.method == 'POST':
        lesson.start_time = request.POST.get('start_time', lesson.start_time)
        lesson.duration = request.POST.get('duration', lesson.duration)

        lesson.save()
        return redirect('schedule:schedule_view')

    context = {
        'lesson': lesson,
    }
    return render(request, 'schedule/edit_lesson.html', context)


@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, teacher=request.user.teacher)
    lesson.delete()
    return redirect('schedule:schedule_view')

