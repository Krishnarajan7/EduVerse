from django import forms
from .models import Student, Subject, Attendance, Fee

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'class_group', 'phone', 'address', 'dob', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'address', 'profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'is_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['amount', 'due_date', 'paid', 'paid_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MarksForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'marks']