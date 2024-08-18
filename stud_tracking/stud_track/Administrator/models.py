from django.db import models

from faculty.models import Semester, Student, Subject


# Create your models here.

class Faculty(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    password=models.CharField(max_length=50)

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

class Admintable(models.Model):
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=50)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    Paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(auto_now_add=True)
    payment_due_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

