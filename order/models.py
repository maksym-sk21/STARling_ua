from django.db import models
from students.models import Student

# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson_count = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
