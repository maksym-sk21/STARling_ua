from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('mark-lesson-conducted/<int:lesson_id>/', views.mark_lesson_conducted, name='mark_lesson_conducted'),
    path('add-lesson/', views.add_lesson, name='add_lesson'),
    path('edit-lesson/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path('delete-lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
]
