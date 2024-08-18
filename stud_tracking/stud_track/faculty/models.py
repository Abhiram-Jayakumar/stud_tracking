from django.db import models



# Create your models here.

class Student(models.Model):
    name =models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField()
    address = models.TextField()
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='student_images/')
    parent_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    

class Parent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()
   

class Semester(models.Model):
    semester_name = models.CharField(max_length=100)

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)

class DisciplinaryRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    disciplinary_action = models.TextField()
    action_date = models.DateField()


class AttendanceUpload(models.Model):
    file = models.FileField(upload_to='attendance/')
    uploaded_at = models.DateTimeField(auto_now_add=True)