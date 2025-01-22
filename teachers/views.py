from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeacherProfileForm, MaterialUploadForm
from django.contrib.auth.decorators import login_required
from .models import Material
from schedule.models import Lesson
from django.utils import timezone
from django.http import HttpResponse, Http404
import mimetypes


def teacher_profile(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            teacher_profile = form.save(commit=False)
            teacher_profile.user = request.user
            teacher_profile.salary = 0
            teacher_profile.save()
            return redirect('teachers:teacher_profile_done')
    else:
        form = TeacherProfileForm()

    return render(request, 'teachers/teacher_profile.html', {'form': form})


def teacher_profile_done(request):
    return render(request, 'teachers/teacher_profile_done.html')


@login_required
def teacher_area(request):
    teacher = request.user.teacher
    materials = teacher.materials.all()
    students = teacher.student.all()
    current_salary = teacher.salary

    lessons = Lesson.objects.filter(teacher=teacher)

    events = []
    for lesson in lessons:
        event = {
            'title': f'{lesson.student.name}',
            'start': lesson.date.isoformat() + 'T' + lesson.start_time.strftime('%H:%M:%S'),
        }
        if lesson.conducted:
            event['classNames'] = ['conducted-lesson']
        events.append(event)

    context = {
        'teacher': teacher,
        'materials': materials,
        'students': students,
        'current_salary': current_salary,
        'events': events,
    }
    return render(request, 'teachers/teacher_area.html', context)


@login_required
def upload_material(request):
    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.teacher = request.user.teacher
            material.name = request.FILES['file'].name
            material.save()
            return redirect('teachers:teacher_area')
    else:
        form = MaterialUploadForm()
    return render(request, 'teachers/upload_material.html', {'form': form})


@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id, teacher=request.user.teacher)
    material.delete()
    return redirect('teachers:teacher_area')


@login_required
def view_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    mime_type, _ = mimetypes.guess_type(material.file.path)

    if not mime_type:
        raise Http404("Unsupported file type.")

    response = HttpResponse(material.file.read(), content_type=mime_type)

    if request.GET.get('download') == 'true':
        response['Content-Disposition'] = f'attachment; filename="{material.file.name}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{material.file.name}"'

    return response