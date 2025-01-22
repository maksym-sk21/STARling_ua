"""
URL configuration for starlingua project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from students.management.commands.telegram_bot import telegram_webhook
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
    path('turnover/', include('turnover.urls')),
    path('schedule/', include('schedule.urls')),
    path('manager/', include('managers.urls')),
    path('webhook/', telegram_webhook, name='telegram_webhook'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
