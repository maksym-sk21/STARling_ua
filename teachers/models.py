from django.db import models
from students.models import Student
from django.conf import settings

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    student = models.ManyToManyField(Student, related_name='teachers')
    phone_number = models.CharField(max_length=20)
    student_phone_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conducted_lessons = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Material(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
