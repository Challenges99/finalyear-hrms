# Generated by Django 5.0.7 on 2024-09-08 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_rename_due_date_task_deadline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
