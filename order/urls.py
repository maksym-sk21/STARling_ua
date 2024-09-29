from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('liqpay_callback/', views.liqpay_callback, name='liqpay_callback'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment/', views.payment_view, name='payment'),  # Ваш основной платежный маршрут
]