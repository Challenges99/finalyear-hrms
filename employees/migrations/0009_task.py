# Generated by Django 5.0.7 on 2024-09-07 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_alter_profile_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('priority', models.CharField(choices=[('High', 'High'), ('Low', 'Low'), ('Medium', 'Medium ')], default='Low', max_length=10)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete')], default='Incomplete', max_length=10)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.profile')),
            ],
        ),
    ]
