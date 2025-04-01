from django.db import models
from django.contrib.auth.models import User
from students.models import Class

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    staffName = models.CharField(max_length=100)
    staffId = models.CharField(max_length=20, unique=True)
    staffEmail = models.EmailField()

    def __str__(self):
        return self.staffName

class Resource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')  # Add this
    uploaded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='resources')
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='resources', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='notices')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    