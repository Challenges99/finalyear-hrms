# Generated by Django 5.0.7 on 2024-09-01 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_profile_address_alter_employer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.profile')),
            ],
        ),
    ]
