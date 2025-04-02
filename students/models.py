from django.db import models
from django.contrib.auth.models import User

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
    name = models.CharField(max_length=100)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='marks')
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.student.name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    class_group = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_classes = models.IntegerField(default=0)
    classes_attended = models.IntegerField(default=0)
    age = models.PositiveIntegerField(null=True, blank=True)  # New field
    dob = models.DateField(null=True, blank=True)  # New field

    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return (self.classes_attended / self.total_classes) * 100

    def __str__(self):
        return self.name