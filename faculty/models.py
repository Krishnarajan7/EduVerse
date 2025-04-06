from django.db import models
from django.contrib.auth.models import User
from students.models import Student

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  
    dob = models.DateField(blank=True, null=True)  
    age = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='faculty_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')
    class_group = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title