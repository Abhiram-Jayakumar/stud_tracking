# Generated by Django 5.1 on 2024-08-17 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administrator', '0009_rename_sem_payment_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='semester',
            new_name='sem',
        ),
    ]
