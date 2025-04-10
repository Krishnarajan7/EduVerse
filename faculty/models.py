from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='faculty_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        from datetime import date
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey('Faculty', on_delete=models.CASCADE, default=1)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class_group = models.ForeignKey('students.Class', on_delete=models.CASCADE)


    def __str__(self):
        return self.title