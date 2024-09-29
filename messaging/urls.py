from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/', views.conversation_view, name='conversation_view'),
]
