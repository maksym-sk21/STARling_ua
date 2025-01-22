from django.shortcuts import render, redirect
from .forms import StudentProfileForm
from schedule.models import Lesson
from .models import Student
from liqpay import LiqPay, LiqPayValidationError
import json
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from turnover.models import Turnover, TotalTurnover, TeacherCalculation, Client, Salary, School
from teachers.models import Teacher, Material
from django.contrib.auth.decorators import login_required

def student_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.save()
            return redirect('students:student_profile_done')
    else:
        form = StudentProfileForm()

    return render(request, 'students/student_profile.html', {'form': form})


def student_profile_done(request):
    return render(request, 'students/student_profile_done.html')


@login_required
def student_area(request):
    student = request.user.student
    materials = Material.objects.filter(teacher__in=student.teachers.all())

    lessons = Lesson.objects.filter(student=student)
    turnovers = Turnover.objects.filter(student=student)

    client = None
    for turnover in turnovers:
        try:
            client = Client.objects.get(turnover=turnover)
            break
        except Client.DoesNotExist:
            continue
    events = [
        {
            'title': f"Урок с {lesson.teacher.name}",
            'start': f"{lesson.date}T{lesson.start_time}",
            'duration': str(lesson.duration),
            'backgroundColor': '#228b22' if lesson.conducted else 'red',
        }
        for lesson in lessons
    ]

    context = {
        'lessons': lessons,
        'materials': materials,
        'events': events,
        'client': client,
    }
    return render(request, 'students/student_area.html', context)


liqpay_client = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)


@login_required
def payment_view(request):
    if request.method == 'POST':
        order_id = str(uuid.uuid4())

        params = {
            'amount': '10.00',
            'currency': 'USD',
            'description': 'Test Payment',
            'result_url': 'http://localhost:8000/students/payment/result/',
            'server_url': 'http://localhost:8000/students/payment/notification/',
            'order_id': order_id  # Передача строкового order_id
        }
        print("Параметры запроса:", params)

        try:
            json_data = json.dumps(params).encode('utf-8')
            liqpay_form = liqpay_client.get_checkout_form(**params)
        except Exception as e:
            print("Ошибка при получении формы:", e)
            return render(request, 'students/error.html', {'error': str(e)})

        print("Форма LiqPay:", liqpay_form)

        return render(request, 'students/payment.html', {'form': liqpay_form})
    else:
        return render(request, 'students/payment.html')


@csrf_exempt
def payment_callback(request):
    # Обработка callback после платежа от LiqPay
    pass
