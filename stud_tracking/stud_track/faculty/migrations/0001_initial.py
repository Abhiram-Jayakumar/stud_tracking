# Generated by Django 5.1 on 2024-08-09 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.ImageField(upload_to='student_images/')),
                ('parent_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
