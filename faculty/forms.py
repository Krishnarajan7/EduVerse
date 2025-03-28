from django import forms
from students.models import Student, Class

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'class_group']
        widgets = {
            'class_group': forms.Select(),
        }