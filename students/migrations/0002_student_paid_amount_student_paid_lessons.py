# Generated by Django 5.0.6 on 2024-07-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='student',
            name='paid_lessons',
            field=models.IntegerField(default=0),
        ),
    ]
