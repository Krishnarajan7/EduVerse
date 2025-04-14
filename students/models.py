from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]

    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    section = models.CharField(max_length=5)
    department = models.CharField(max_length=50, default='CSE')

    def __str__(self):
        return f"{self.year} {self.department} {self.section}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True) 
    phone = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    classes_attended = models.PositiveIntegerField(default=0)
    total_classes = models.PositiveIntegerField(default=0)
    changed_password = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    admission_type = models.CharField(max_length=50, choices=[('Regular', 'Regular'), ('Special', 'Special')], blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    @property
    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return (self.classes_attended / self.total_classes) * 100

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

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        status = 'Present' if self.is_present else 'Absent'
        return f"{self.student.name} - {self.date} - {status}"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    def __str__(self):
        status = 'Paid' if self.paid else 'Unpaid'
        return f"{self.student.name} - ₹{self.amount} - {status}"