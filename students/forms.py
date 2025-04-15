from django import forms
from .models import Student, Subject, Attendance, Fee
import re

class StudentForm(forms.ModelForm):
    """Form for creating or editing a student instance (admin-side)."""
    class Meta:
        model = Student
        fields = [
            'name', 'roll_number', 'email', 'class_group',
            'phone', 'address', 'dob', 'profile_picture'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'profile_picture': forms.ClearableFileInput(),
        }
        labels = {
            'dob': 'Date of Birth',
            'class_group': 'Class',
        }


class StudentProfileForm(forms.ModelForm):
    """Form for student to edit their own profile."""
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput())

    class Meta:
        model = Student
        fields = ['phone', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'phone': 'Phone Number',
            'address': 'Residential Address',
        }


class AttendanceForm(forms.ModelForm):
    """Form for adding/updating student attendance."""
    class Meta:
        model = Attendance
        fields = ['date', 'is_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'is_present': 'Present?',
        }


class FeeForm(forms.ModelForm):
    """Form for creating/updating fee records."""
    class Meta:
        model = Fee
        fields = ['amount', 'due_date', 'paid', 'paid_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'due_date': 'Due Date',
            'paid_date': 'Date Paid',
        }


class MarksForm(forms.ModelForm):
    """Form for entering/updating subject marks."""
    class Meta:
        model = Subject
        fields = ['name', 'marks']
        labels = {
            'name': 'Subject Name',
            'marks': 'Marks Obtained',
        }


class ChangePasswordForm(forms.Form):
    """Custom form to allow users to securely change their password."""
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        # Optional: Add regex for stronger password
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$'
        if not re.match(password_regex, new_password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter, one number, and one special character."
            )
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data
