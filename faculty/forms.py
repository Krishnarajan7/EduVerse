from django import forms
from students.models import Student, Class
from faculty.models import Notice, Resource, Faculty  # Import Faculty
from students.models import Subject
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'class_group', 'phone', 'address', 'age', 'dob']

    def save(self, commit=True):
        student = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        student.user = user
        if commit:
            student.save()
        return student

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['classes_attended', 'total_classes']

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
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Faculty
        fields = ['name', 'email', 'phone', 'age', 'dob']

    def save(self, commit=True):
        faculty = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        faculty.user = user
        if commit:
            faculty.save()
        return faculty