from django.db import models
from django.contrib.auth.models import User
from students.models import Class

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    staff_name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)
    staff_email = models.EmailField()
    
    def __str__(self):
        return self.staff_name 
    
class Resource(models.Model):
    title = models.CharField(max_length=200)
    files = models.FileField(upload_to='resources/')
    uploaded_to = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='resources') 
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='resources', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title