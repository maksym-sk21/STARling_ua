from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'teachers'

urlpatterns = [
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('profile/done/', views.teacher_profile_done, name='teacher_profile_done'),
    path('my_profile', views.teacher_area, name='teacher_area'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('view-material/<int:material_id>/', views.view_material, name='view_material'),
    path('delete-material/<int:material_id>/', views.delete_material, name='delete_material'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
