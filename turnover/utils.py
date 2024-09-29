import pandas as pd
from django.core.management.base import BaseCommand
from turnover.models import Turnover, School, Salary, Client, TeacherCalculation
from django.utils import timezone
from decimal import Decimal

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

        with pd.ExcelWriter(f'turnover_{start_date.date()}_to_{end_date.date()}.xlsx') as writer:
            pd.DataFrame(list(turnovers.values())).to_excel(writer, sheet_name='Turnovers')
            pd.DataFrame(list(schools.values())).to_excel(writer, sheet_name='Schools')
            pd.DataFrame(list(salaries.values())).to_excel(writer, sheet_name='Salaries')
            pd.DataFrame(list(clients.values())).to_excel(writer, sheet_name='Clients')
            pd.DataFrame(list(teacher_calculations.values())).to_excel(writer, sheet_name='TeacherCalculations')

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
