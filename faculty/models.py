from django.db import models
from django.contrib.auth.models import User
from students.models import Class, Student, Subject  

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='faculty_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class FacultyIncharge(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_group = models.OneToOneField(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.name} - Incharge of {self.class_group.name}"


class FacultyTimetable(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'),
    ]
    PERIOD_CHOICES = [(i, f'Period {i}') for i in range(1, 9)]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    period_number = models.IntegerField(choices=PERIOD_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.name} - {self.class_group.name} - {self.day} P{self.period}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField()
    is_present = models.BooleanField()

    class Meta:
        unique_together = ('student', 'date', 'period')

    def __str__(self):
        return f"{self.student.name} - {self.date} - P{self.period} - {'Present' if self.is_present else 'Absent'}"


class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class FacultyPeriodAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_group = models.ForeignKey('students.Class', on_delete=models.CASCADE)
    subject = models.ForeignKey('students.Subject', on_delete=models.CASCADE)
    day = models.CharField(max_length=10)  
    period_number = models.PositiveIntegerField()  

    class Meta:
        unique_together = ('class_group', 'day', 'period_number')

    def __str__(self):
        return f"{self.faculty.name} teaches {self.subject.name} in {self.class_group.name} on {self.day}, Period {self.period_number}"



