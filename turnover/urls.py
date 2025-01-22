from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'turnover'

urlpatterns = [
    path('manage/', views.manage_turnover, name='manage_turnover'),
    path('manage/edit/<int:pk>/', views.edit_turnover, name='edit_turnover'),
    path('manage/add/', views.add_turnover, name='add_turnover'),
    path('manage/school/', views.manage_school, name='manage_school'),
    path('manage/school/edit/<int:pk>/', views.edit_school, name='edit_school'),
    path('manage/school/add/', views.add_school, name='add_school'),
    path('manage/salary/', views.manage_salary, name='manage_salary'),
    path('manage/salary/edit/<int:pk>/', views.edit_salary, name='edit_salary'),
    path('manage/salary/add/', views.add_salary, name='add_salary'),
    path('manage/client/', views.manage_client, name='manage_client'),
    path('manage/client/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('manage/client/add/', views.add_client, name='add_client'),
    path('manage/teacher_calculation/', views.manage_teacher_calculation, name='manage_teacher_calculation'),
    path('manage/teacher_calculation/edit/<int:pk>/', views.edit_teacher_calculation, name='edit_teacher_calculation'),
    path('manage/teacher_calculation/add/', views.add_teacher_calculation, name='add_teacher_calculation'),
    path('manage/total_turnover/', views.manage_total_turnover, name='manage_total_turnover'),
    path('manage/total_turnover/edit/<int:pk>/', views.edit_total_turnover, name='edit_total_turnover'),
    path('manage/turnover/delete/<int:pk>/', views.delete_turnover, name='delete_turnover'),
    path('manage/teacher_calculation/delete/<int:pk>/', views.delete_teacher_calculation,
         name='delete_teacher_calculation'),
    path('manage/school/delete/<int:pk>/', views.delete_school, name='delete_school'),
    path('manage/client/delete/<int:pk>/', views.delete_client, name='delete_client'),
    path('manage/salary/delete/<int:pk>/', views.delete_salary, name='delete_salary'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('students/', views.student_list, name='student_list'),
    path('assign_student/<int:teacher_id>/', views.assign_student, name='assign_student'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('assign_student/<int:teacher_id>/', views.assign_student, name='assign_student'),
    path('unassign_student/<int:teacher_id>/<int:student_id>/', views.unassign_student, name='unassign_student'),
    path('schedule/', views.manage_schedule, name='manage_schedule'),
    path('add_lesson', views.add_lesson, name='add_lesson'),
    path('edit_lesson/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)