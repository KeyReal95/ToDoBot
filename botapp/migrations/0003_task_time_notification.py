# Generated by Django 4.0.4 on 2022-05-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0002_alter_task_name_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='time_notification',
            field=models.TimeField(null=True, verbose_name='Время напоминания'),
        ),
    ]
