from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse, JsonResponse, Http404
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import mimetypes
from django.shortcuts import get_object_or_404
from teachers.models import Teacher


@login_required
def manager_area(request):
    teachers = Teacher.objects.all()
    if request.method == "POST" and request.POST.get("update_period"):
        call_command("update_period")
        return JsonResponse({"message": "Успешно обновлено"}, status=200)

    export_path = os.path.join(settings.MEDIA_ROOT, 'turnover_exports')
    report_files = []
    if os.path.exists(export_path):
        report_files = [f for f in os.listdir(export_path) if f.endswith('.xlsx')]

    context = {
        'report_files': report_files,
        "teachers": teachers,
    }
    return render(request, 'managers/manager_area.html', context)


def view_report(request, report_filename):
    report_path = os.path.join(settings.MEDIA_ROOT, 'turnover_exports', report_filename)

    if not os.path.exists(report_path):
        raise Http404("Report not found.")

    mime_type, _ = mimetypes.guess_type(report_path)
    if not mime_type:
        raise Http404("Unsupported file type.")

    with open(report_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=mime_type)

    if request.GET.get('download') == 'true':
        response['Content-Disposition'] = f'attachment; filename="{report_filename}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{report_filename}"'

    return response