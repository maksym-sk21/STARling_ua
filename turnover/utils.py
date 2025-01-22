import pandas as pd
from django.core.management.base import BaseCommand
from turnover.models import Turnover, School, Salary, Client, TeacherCalculation
from students.models import Student
from teachers.models import Teacher
from django.utils import timezone
from decimal import Decimal
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Update turnover data and export to Excel at the end of each period'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        if now.day <= 15:
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(day=15, hour=23, minute=59, second=59, microsecond=999999)
        else:
            start_date = now.replace(day=16, hour=0, minute=0, second=0, microsecond=0)
            next_month = (now.replace(day=1) + timezone.timedelta(days=31)).replace(day=1)
            end_date = next_month - timezone.timedelta(seconds=1)

        turnovers = Turnover.objects.filter(date__range=[start_date, end_date])
        schools = School.objects.filter(turnover__in=turnovers)
        salaries = Salary.objects.filter(turnover__in=turnovers)
        clients = Client.objects.filter(turnover__in=turnovers)
        teacher_calculations = TeacherCalculation.objects.filter(turnover__in=turnovers)

        export_path = os.path.join(settings.MEDIA_ROOT, 'turnover_exports')
        os.makedirs(export_path, exist_ok=True)
        file_path = os.path.join(export_path,  f'turnover_{start_date.date()}_to_{end_date.date()}.xlsx')

        with pd.ExcelWriter(file_path) as writer:
            students_dict = {student.id: student.name for student in Student.objects.all()}
            teachers_dict = {teacher.id: teacher.name for teacher in Teacher.objects.all()}

            turnover_df = pd.DataFrame(list(turnovers.values()))

            turnover_df['student_id'] = turnover_df['student_id'].map(students_dict)
            turnover_df['teacher_id'] = turnover_df['teacher_id'].map(teachers_dict)

            turnover_df.rename(columns={
                'id': 'ID',
                'date': 'Дата',
                'student_id': 'Студент',
                'teacher_id': 'Вчитель',
                'previous_hours': 'Попередні години',
                'previous_balance': 'Попередній баланс',
                'current_hours': 'Поточні години',
                'current_payment': 'Поточний платіж',
                'total_hours': 'Загальні години',
                'profit': 'Прибуток',
            }, inplace=True)

            turnover_df.to_excel(writer, sheet_name='Оборот')

            school_df = pd.DataFrame(list(schools.values()))
            school_df.rename(columns={
                'turnover': 'Оборот',
                'total_profit': 'Общая прибыль',
                'school_budget': 'Бюджет школы',
                'budget_elena': 'Бюджет Елены',
                'budget_maria': 'Бюджет Марии',
            }, inplace=True)
            school_df.to_excel(writer, sheet_name='Школа')

            salary_df = pd.DataFrame(list(salaries.values()))
            salary_df.rename(columns={
                'turnover': 'Оборот',
                'monthly_profit': 'Ежемесячная прибыль',
                'monthly_budget': 'Ежемесячный бюджет',
                'salary_elena': 'Зарплата Елены',
                'salary_maria': 'Зарплата Марии'
            }, inplace=True)
            salary_df.to_excel(writer, sheet_name='Зарплати')

            client_df = pd.DataFrame(list(clients.values()))
            client_df.rename(columns={
                'turnover': 'Оборот',
                'hourly_rate': 'Ставка за годину',
                'money_spent': 'Потраченные деньги',
                'remaining_hours': 'Залишкові години',
                'remaining_money': 'Залишкова сума',
            }, inplace=True)

            client_df.to_excel(writer, sheet_name='Клієнти')

            teacher_calc_df = pd.DataFrame(list(teacher_calculations.values()))
            teacher_calc_df.rename(columns={
                'turnover': 'Оборот',
                'hourly_rate': 'Почасовая ставка',
                'hours_spent': 'Потраченные часы',
                'salary_teacher': 'Зарплата преподавателя',
                'budget_teacher': 'Бюджет преподавателя',
            }, inplace=True)

            teacher_calc_df.to_excel(writer, sheet_name='Розрахунки викладачів')

        self.stdout.write(self.style.SUCCESS(f'Successfully exported data from {start_date.date()} to {end_date.date()}'))

        self.update_turnover_for_new_period(start_date, end_date)

    def update_turnover_for_new_period(self, start_date, end_date):
        now = timezone.now()
        current_turnovers = Turnover.objects.filter(date__range=[start_date, end_date])
        turnover_data = list(current_turnovers.values())

        old_client_data = {
            client.turnover_id: {
                'remaining_hours': client.remaining_hours,
                'remaining_money': client.remaining_money,
                'hourly_rate': client.hourly_rate
            }
            for client in Client.objects.filter(turnover__in=current_turnovers)
        }

        old_teacher_calc_data = {
            teacher_calc.turnover_id: {
                'hourly_rate': teacher_calc.hourly_rate
            }
            for teacher_calc in TeacherCalculation.objects.filter(turnover__in=current_turnovers)
        }

        current_turnovers.delete()

        for data in turnover_data:
            old_client = old_client_data.get(data['id'], {})
            old_client_remaining_hours = old_client.get('remaining_hours', Decimal('0.00'))
            old_client_remaining_money = old_client.get('remaining_money', Decimal('0.00'))
            old_client_hourly_rate = old_client.get('hourly_rate', Decimal('0.00'))

            new_turnover = Turnover.objects.create(
                student_id=data['student_id'],
                teacher_id=data['teacher_id'],
                previous_hours=old_client_remaining_hours,
                previous_balance=old_client_remaining_money,
                current_hours=0,
                current_payment=0,
                total_hours=data['current_hours'],
                profit=data['current_payment'],
                date=now
            )
            print(f"Created new turnover: {new_turnover}")

            client = Client.objects.get(turnover=new_turnover)
            client.hourly_rate = old_client_hourly_rate
            client.save(update_fields=['hourly_rate'])

            teacher_calc = TeacherCalculation.objects.get(turnover=new_turnover)
            teacher_calc.hourly_rate = old_teacher_calc_data.get(data['id'], {}).get('hourly_rate', Decimal('0.00'))
            teacher_calc.save(update_fields=['hourly_rate'])
