from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    path('my_profile/', views.manager_area, name='manager_area'),
]
