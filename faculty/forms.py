from django import forms
from students.models import Student, Class
from .models import Resource  # This should now work

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'class_group']
        widgets = {
            'class_group': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Class queryset:", self.fields['class_group'].queryset)

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
        widgets = {
            'class_group': forms.Select(),
        }