from django.contrib import admin
from .models import Student, Attendance, Fee, Subject

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'phone')
    search_fields = ('name', 'roll_number')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    list_filter = ('date', 'is_present')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'due_date', 'paid')
    list_filter = ('paid', 'due_date')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'marks')
    list_filter = ('name',)
    search_fields = ('student__name', 'student__roll_number')