# Generated by Django 5.1 on 2024-08-16 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
