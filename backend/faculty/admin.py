from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Faculty, FacultyIncharge, FacultyTimetable, Attendance, Notice, Resource, FacultyPeriodAssignment


admin.site.register(Faculty)
admin.site.register(FacultyIncharge)
admin.site.register(FacultyTimetable)
admin.site.register(Attendance)
admin.site.register(Notice)
admin.site.register(Resource)
admin.site.register(FacultyPeriodAssignment)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'role')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = UserAdmin.fieldsets

    def role(self, obj):
        if obj.is_superuser:
            return 'Admin'
        group = obj.groups.first()
        return group.name if group else 'Faculty'
    role.short_description = 'Role'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)