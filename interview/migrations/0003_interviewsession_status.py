# Generated by Django 5.1.7 on 2025-04-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_interviewhistory_last_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewsession',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='scheduled', max_length=25),
        ),
    ]
