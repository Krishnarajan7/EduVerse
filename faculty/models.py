from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    staffName = models.CharField(max_length=100)
    staffId = models.CharField(max_length=20, unique=True)
    staffEmail = models.EmailField()
    
    def __str__(self):
        return self.staffName