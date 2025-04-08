from django.contrib import admin
from .models import Student,Class,Subject,Attendance,Fee

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Fee)
