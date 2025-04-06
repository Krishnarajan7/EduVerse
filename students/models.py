from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    class_group = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    classes_attended = models.IntegerField(default=0)
    total_classes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Class(models.Model):
    year = models.CharField(max_length=10, choices=[
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ])
    section = models.CharField(max_length=5)
    department = models.CharField(max_length=50, default='CSE')

    def __str__(self):
        return f"{self.year} {self.department} {self.section}"

class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.student.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount} - {'Paid' if self.paid else 'Unpaid'}"