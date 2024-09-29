from django.db import models
from django.conf import settings


class Student(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=50)
    lesson_count = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True, null=True)
    paid_lessons = models.IntegerField(default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    lesson_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.name
