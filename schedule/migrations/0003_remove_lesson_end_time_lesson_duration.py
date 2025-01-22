# Generated by Django 5.0.6 on 2024-08-19 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_rename_time_lesson_start_time_lesson_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='end_time',
        ),
        migrations.AddField(
            model_name='lesson',
            name='duration',
            field=models.DecimalField(choices=[(0.5, '0.5 часа'), (1.0, '1 час'), (1.5, '1.5 часа'), (2.0, '2 часа')], decimal_places=1, default=0, max_digits=2),
        ),
    ]
