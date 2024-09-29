from django.shortcuts import render
from .forms import LessonPaymentForm
from .models import Order
from django.conf import settings
from liqpay import LiqPay
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64
import hashlib
import time
from django.shortcuts import get_object_or_404


LANGUAGE_PRICES = {
    'english': 400,
    'german': 550,
}


def generate_signature(data, private_key):
    sign_string = private_key + data + private_key
    signature = base64.b64encode(hashlib.sha1(sign_string.encode('utf-8')).digest()).decode('utf-8')
    return signature


def payment_view(request):
    if request.method == 'POST':
        form = LessonPaymentForm(request.POST)
        if form.is_valid():
            lesson_count = form.cleaned_data['lesson_count']
            language = form.cleaned_data['language']
            amount = lesson_count * LANGUAGE_PRICES[language]

            student = request.user.student  # Предполагается, что у пользователя есть связанный объект Student

            order_id = f'order_{int(time.time())}'  # Уникальный идентификатор заказа

            Order.objects.create(
                order_id=order_id,
                student=student,
                lesson_count=lesson_count,
                status='pending'
            )

            params = {
                'action': 'pay',
                'amount': amount,
                'currency': 'UAH',
                'description': f'Оплата за {lesson_count} уроков {language}',
                'order_id': order_id,
                'version': '3',
                'sandbox': int(settings.LIQPAY_SANDBOX_MODE),
                'server_url': request.build_absolute_uri(reverse('order:liqpay_callback')),
                'result_url': request.build_absolute_uri(reverse('order:payment_success')),
            }

            data = base64.b64encode(json.dumps(params).encode('utf-8')).decode('utf-8')
            signature = generate_signature(data, settings.LIQPAY_PRIVATE_KEY)

            form_data = {
                'data': data,
                'signature': signature,
            }

            return render(request, 'order/payment_form.html', {'form_data': form_data})

    else:
        form = LessonPaymentForm()

    return render(request, 'order/payment.html', {'form': form})


@csrf_exempt
def liqpay_callback(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        signature = request.POST.get('signature')

        expected_signature = generate_signature(data, settings.LIQPAY_PRIVATE_KEY)

        if signature == expected_signature:
            response_data = json.loads(base64.b64decode(data).decode('utf-8'))
            order_id = response_data['order_id']
            status = response_data['status']

            if status == 'success':
                try:
                    # Найдите заказ по идентификатору
                    order = get_object_or_404(Order, order_id=order_id)
                    student = order.student  # Предполагается, что у заказа есть связь с учеником
                    lesson_count = order.lesson_count  # Предполагается, что у заказа есть количество уроков

                    # Обновите количество оплаченных уроков у ученика
                    student.paid_lessons += lesson_count
                    student.save()

                    # Обновите статус заказа
                    order.status = 'paid'
                    order.save()

                    return JsonResponse({'status': 'success'})
                except Order.DoesNotExist:
                    return JsonResponse({'status': 'order not found'}, status=404)
            else:
                return JsonResponse({'status': 'payment not successful'}, status=400)
        else:
            return JsonResponse({'status': 'invalid signature'}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=400)


def payment_success(request):
    return render(request, 'turnover/payment_success.html')