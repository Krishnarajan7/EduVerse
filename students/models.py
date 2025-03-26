from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Faculty(models.Model):
    staffName = models.CharField(max_length=100)
    staffId = models.CharField(max_length=20, unique=True)
    staffEmail = models.EmailField()
    
    def __str__(self):
        return self.staffName