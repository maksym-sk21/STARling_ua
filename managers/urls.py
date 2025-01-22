from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'managers'

urlpatterns = [
    path('my_profile/', views.manager_area, name='manager_area'),
    path('view_report/<str:report_filename>/', views.view_report, name='view_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
