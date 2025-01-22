from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Turnover, TotalTurnover, TeacherCalculation, Client, Salary, School
from .forms import (TurnoverForm, TotalTurnoverForm, ClientForm, SalaryForm, SchoolForm,
                    TeacherCalculationForm, AssignStudentForm, StudentForm, TeacherForm)
from schedule.forms import LessonForm
from teachers.models import Teacher
from students.models import Student
from schedule.models import Lesson



def is_manager(user):
    return user.groups.filter(name='Managers').exists()


@login_required
@user_passes_test(is_manager)
def manage_turnover(request):
    turnovers = Turnover.objects.all()
    total = turnovers.aggregate(
        total_previous_hours=Sum('previous_hours'),
        total_previous_balance=Sum('previous_balance'),
        total_current_hours=Sum('current_hours'),
        total_current_payment=Sum('current_payment'),
        total_profit=Sum('profit')

    )
    return render(request, 'turnover/manage_turnover.html', {'turnovers': turnovers, 'total': total})


@login_required
@user_passes_test(is_manager)
def edit_turnover(request, pk):
    turnover = get_object_or_404(Turnover, pk=pk)
    if request.method == 'POST':
        form = TurnoverForm(request.POST, instance=turnover)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_turnover')
    else:
        form = TurnoverForm(instance=turnover)
    return render(request, 'turnover/edit_turnover.html', {'form': form, 'turnover': turnover})


@login_required
@user_passes_test(is_manager)
def add_turnover(request):
    if request.method == 'POST':
        form = TurnoverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_turnover')
    else:
        form = TurnoverForm()
    return render(request, 'turnover/add_turnover.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def manage_school(request):
    schools = School.objects.all()
    total = schools.aggregate(
        total_total_profit=Sum('total_profit'),
        total_school_budget=Sum('school_budget'),
        total_budget_elena=Sum('budget_elena'),
        total_budget_maria=Sum('budget_maria')
    )
    return render(request, 'turnover/manage_school.html', {'schools': schools, 'total': total})


@login_required
@user_passes_test(is_manager)
def edit_school(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_school')
    else:
        form = SchoolForm(instance=school)
    return render(request, 'turnover/edit_school.html', {'form': form, 'school': school})


@login_required
@user_passes_test(is_manager)
def add_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_school')
    else:
        form = SchoolForm()
    return render(request, 'turnover/add_school.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def manage_salary(request):
    salaries = Salary.objects.all()
    total = salaries.aggregate(
        total_monthly_profit=Sum('monthly_profit'),
        total_monthly_budget=Sum('monthly_budget'),
        total_salary_elena=Sum('salary_elena'),
        total_salary_maria=Sum('salary_maria')
    )
    return render(request, 'turnover/manage_salary.html', {'salaries': salaries, 'total': total})


@login_required
@user_passes_test(is_manager)
def edit_salary(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_salary')
    else:
        form = SalaryForm(instance=salary)
    return render(request, 'turnover/edit_salary.html', {'form': form, 'salary': salary})


@login_required
@user_passes_test(is_manager)
def add_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_salary')
    else:
        form = SalaryForm()
    return render(request, 'turnover/add_salary.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def manage_client(request):
    clients = Client.objects.all()
    total = clients.aggregate(
        avg_hourly_rate=Avg('hourly_rate'),
        total_money_spent=Sum('money_spent'),
        total_remaining_hours=Sum('remaining_hours')
    )
    return render(request, 'turnover/manage_client.html', {'clients': clients, 'total': total})


@login_required
@user_passes_test(is_manager)
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_client')
    else:
        form = ClientForm(instance=client)
    return render(request, 'turnover/edit_client.html', {'form': form, 'client': client})


@login_required
@user_passes_test(is_manager)
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_client')
    else:
        form = ClientForm()
    return render(request, 'turnover/add_client.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def manage_teacher_calculation(request):
    teacher_calculations = TeacherCalculation.objects.all()
    total = teacher_calculations.aggregate(
        avg_hourly_rate=Avg('hourly_rate'),
        total_salary_teacher=Sum('salary_teacher'),
        total_hours_spent=Sum('hours_spent')
    )
    return render(request, 'turnover/manage_teacher_calculation.html', {'teacher_calculations': teacher_calculations, 'total': total})


@login_required
@user_passes_test(is_manager)
def edit_teacher_calculation(request, pk):
    teacher_calculation = get_object_or_404(TeacherCalculation, pk=pk)
    if request.method == 'POST':
        form = TeacherCalculationForm(request.POST, instance=teacher_calculation)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_teacher_calculation')
    else:
        form = TeacherCalculationForm(instance=teacher_calculation)
    return render(request, 'turnover/edit_teacher_calculation.html', {'form': form, 'teacher_calculation': teacher_calculation})


@login_required
@user_passes_test(is_manager)
def add_teacher_calculation(request):
    if request.method == 'POST':
        form = TeacherCalculationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_teacher_calculation')
    else:
        form = TeacherCalculationForm()
    return render(request, 'turnover/add_teacher_calculation.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def manage_total_turnover(request):
    total_previous_hours = Turnover.objects.aggregate(Sum('previous_hours'))['previous_hours__sum'] or 0
    total_previous_balance = Turnover.objects.aggregate(Sum('previous_balance'))['previous_balance__sum'] or 0
    total_current_hours = Turnover.objects.aggregate(Sum('current_hours'))['current_hours__sum'] or 0
    total_current_payment = Turnover.objects.aggregate(Sum('current_payment'))['current_payment__sum'] or 0
    total_total_hours = Turnover.objects.aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    total_profit = Turnover.objects.aggregate(Sum('profit'))['profit__sum'] or 0

    total_school_budget = School.objects.aggregate(Sum('school_budget'))['school_budget__sum'] or 0
    total_budget_elena = School.objects.aggregate(Sum('budget_elena'))['budget_elena__sum'] or 0
    total_budget_maria = School.objects.aggregate(Sum('budget_maria'))['budget_maria__sum'] or 0

    total_salary_elena = Salary.objects.aggregate(Sum('salary_elena'))['salary_elena__sum'] or 0
    total_salary_maria = Salary.objects.aggregate(Sum('salary_maria'))['salary_maria__sum'] or 0
    total_monthly_profit = Salary.objects.aggregate(Sum('monthly_profit'))['monthly_profit__sum'] or 0
    total_monthly_budget = Salary.objects.aggregate(Sum('monthly_budget'))['monthly_budget__sum'] or 0

    total_hourly_rate = TeacherCalculation.objects.aggregate(Avg('hourly_rate'))['hourly_rate__sum'] or 0
    total_hours_spent = TeacherCalculation.objects.aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
    total_money_spent = Client.objects.aggregate(Sum('money_spent'))['money_spent__sum'] or 0
    total_remaining_hours = Client.objects.aggregate(Sum('remaining_hours'))['remaining_hours__sum'] or 0

    context = {
        'total_turnovers': [{
            'total_previous_hours': total_previous_hours,
            'total_previous_balance': total_previous_balance,
            'total_current_hours': total_current_hours,
            'total_current_payment': total_current_payment,
            'total_total_hours': total_total_hours,
            'total_profit': total_profit,
            'total_school_budget': total_school_budget,
            'total_budget_elena': total_budget_elena,
            'total_budget_maria': total_budget_maria,
            'total_salary_elena': total_salary_elena,
            'total_salary_maria': total_salary_maria,
            'total_monthly_profit': total_monthly_profit,
            'total_monthly_budget': total_monthly_budget,
            'total_hours_spent': total_hours_spent,
            'total_hourly_rate': total_hourly_rate,
            'total_money_spent': total_money_spent,
            'total_remaining_hours': total_remaining_hours,
        }]
    }

    return render(request, 'turnover/manage_total_turnover.html', context)


@login_required
@user_passes_test(is_manager)
def edit_total_turnover(request, pk):
    total_turnover = get_object_or_404(TotalTurnover, pk=pk)
    if request.method == 'POST':
        form = TotalTurnoverForm(request.POST, instance=total_turnover)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_total_turnover')
    else:
        form = TotalTurnoverForm(instance=total_turnover)
    return render(request, 'turnover/edit_total_turnover.html', {'form': form, 'total_turnover': total_turnover})


@login_required
@user_passes_test(is_manager)
def delete_turnover(request, pk):
    turnover = get_object_or_404(Turnover, pk=pk)
    turnover.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_turnover')


@login_required
@user_passes_test(is_manager)
def delete_teacher_calculation(request, pk):
    teacher_calculation = get_object_or_404(TeacherCalculation, pk=pk)
    teacher_calculation.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_teacher_calculation')


@login_required
@user_passes_test(is_manager)
def delete_school(request, pk):
    school = get_object_or_404(School, pk=pk)
    school.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_school')


@login_required
@user_passes_test(is_manager)
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_client')


@login_required
@user_passes_test(is_manager)
def delete_salary(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    salary.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_salary')


@login_required
@user_passes_test(is_manager)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'turnover/teacher_list.html', {'teachers': teachers})


@login_required
@user_passes_test(is_manager)
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'turnover/add_teacher.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'turnover/student_list.html', {'students': students})


@login_required
@user_passes_test(is_manager)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:student_list')
    else:
        form = StudentForm()
    return render(request, 'turnover/add_student.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def assign_student(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = AssignStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            teacher.student.add(student)
            return redirect('turnover:teacher_list')
    else:
        form = AssignStudentForm()
    return render(request, 'turnover/assign_student.html', {'form': form, 'teacher': teacher})


@login_required
@user_passes_test(is_manager)
def unassign_student(teacher_id, student_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = get_object_or_404(Student, id=student_id)
    teacher.student.remove(student)
    return redirect('turnover:teacher_list')


@login_required
@user_passes_test(is_manager)
def delete_teacher(teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect('turnover:teacher_list')


@login_required
@user_passes_test(is_manager)
def delete_student(student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('turnover:student_list')


@login_required
@user_passes_test(is_manager)
def manage_schedule(request):
    lessons = Lesson.objects.all().order_by('date')
    return render(request, 'turnover/manage_schedule.html', {'lessons': lessons})


@login_required
@user_passes_test(is_manager)
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_schedule')
    else:
        form = LessonForm()
    return render(request, 'turnover/add_lesson.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('turnover:manage_schedule')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'turnover/edit_lesson.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    messages.success(request, "Запись успешно удалена.")
    return redirect('turnover:manage_schedule')
