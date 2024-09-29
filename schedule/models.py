from django.db import models
from students.models import Student
from teachers.models import Teacher
from django.utils import timezone


class Lesson(models.Model):
    DURATION_CHOICES = [
        (0.5, '0.5 часа'),
        (1.0, '1 час'),
        (1.5, '1.5 часа'),
        (2.0, '2 часа'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(default="00:00")
    duration = models.DecimalField(max_digits=2, decimal_places=1, choices=DURATION_CHOICES, default=0)
    conducted = models.BooleanField(default=False)

    def __str__(self):
        return f"Lesson: {self.student} with {self.teacher} on {self.date}"
