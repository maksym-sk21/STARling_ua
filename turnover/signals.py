from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Turnover, Client, TeacherCalculation, School, Salary, TotalTurnover
from decimal import Decimal


@receiver(post_save, sender=Turnover)
def update_related_models(sender, instance, created, **kwargs):
    if created:
        teacher_calc, _ = TeacherCalculation.objects.get_or_create(turnover=instance)
        client, _ = Client.objects.get_or_create(turnover=instance)
        school, _ = School.objects.get_or_create(turnover=instance)
        salary, _ = Salary.objects.get_or_create(turnover=instance)
        total_turnover, _ = TotalTurnover.objects.get_or_create(id=1)
    else:
        teacher_calc = TeacherCalculation.objects.get(turnover=instance)
        client = Client.objects.get(turnover=instance)
        school = School.objects.get(turnover=instance)
        salary = Salary.objects.get(turnover=instance)
        total_turnover, _ = TotalTurnover.objects.get_or_create(id=1)

    if client.hourly_rate is not None and client.hourly_rate is not None:
        client.remaining_hours = instance.total_hours - teacher_calc.hours_spent
        client.remaining_money = instance.profit - client.money_spent
        client.save()

    if client.money_spent is not None and teacher_calc.salary_teacher is not None:
        monthly_profit = client.money_spent - teacher_calc.salary_teacher
        salary.monthly_profit = monthly_profit
        salary.monthly_budget = monthly_profit * Decimal('0.30')
        salary.salary_elena = monthly_profit * Decimal('0.40')
        salary.salary_maria = monthly_profit * Decimal('0.30')
        salary.save()


@receiver(pre_save, sender=TeacherCalculation)
def update_teacher_budget(sender, instance, **kwargs):
    if kwargs.get('update_fields') and 'budget_teacher' in kwargs['update_fields']:
        return

    if instance.hourly_rate > 0:
        new_budget = instance.turnover.total_hours * instance.hourly_rate
        if instance.budget_teacher != new_budget:
            instance.budget_teacher = new_budget
            instance.save(update_fields=['budget_teacher'])
            update_school_budget(instance)


@receiver(pre_save, sender=Turnover)
def update_teacher_budget_on_turnover_change(sender, instance, **kwargs):
    if instance.pk:
        previous_turnover = Turnover.objects.get(pk=instance.pk)
        if previous_turnover.profit != instance.profit or previous_turnover.total_hours != instance.total_hours:
            teacher_calc = TeacherCalculation.objects.get(turnover=instance)
            new_budget = instance.total_hours * teacher_calc.hourly_rate
            teacher_calc.budget_teacher = new_budget
            teacher_calc.save(update_fields=['budget_teacher'])


def update_school_budget(teacher_calc):
    turnover = teacher_calc.turnover
    school = School.objects.get(turnover=turnover)
    total_profit = turnover.profit - teacher_calc.budget_teacher
    school.total_profit = total_profit
    school.school_budget = total_profit * Decimal('0.30')
    school.budget_elena = total_profit * Decimal('0.40')
    school.budget_maria = total_profit * Decimal('0.30')
    school.save()


@receiver(post_save, sender=TeacherCalculation)
def update_teacher_salary(sender, instance, **kwargs):
    teacher = instance.turnover.teacher
    teacher.salary = instance.salary_teacher
    teacher.save()
