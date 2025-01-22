from django.contrib import admin
from .models import School, Salary, Turnover, Client, TeacherCalculation, TotalTurnover

# Register your models here.
admin.site.register(Turnover)
admin.site.register(School)
admin.site.register(Salary)
admin.site.register(Client)
admin.site.register(TeacherCalculation)
admin.site.register(TotalTurnover)