from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('student', 'Ученик'), ('teacher', 'Учитель')])

    def __str__(self):
        return self.user.username
