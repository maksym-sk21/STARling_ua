from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/done/', views.student_profile_done, name='student_profile_done'),
    path('my_profile', views.student_area, name='student_area'),
    path('payment/', views.payment_view, name='payment_url'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]
