from django import forms
from students.models import Student, Class, Subject
from .models import Notice, Resource, Faculty

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'class_group', 'phone', 'address', 'age', 'dob', 'total_classes', 'classes_attended', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['total_classes', 'classes_attended']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'marks']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file', 'class_group']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'email', 'phone', 'age', 'dob', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(),
        }