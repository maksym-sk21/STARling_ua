from django.contrib.auth.models import User
from django.db import models


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
