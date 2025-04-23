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
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password",
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        required=False,
        min_length=12,
        help_text="Leave blank to keep current password. Must be at least 12 characters long and include one uppercase, one lowercase, one number, and one special character (e.g., !@#$%)."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password",
        required=False
    )

    class Meta:
        model = Student
        fields = ['phone', 'address', 'profile_picture', 'father_name', 'mother_name', 'parent_phone', 'community', 'place_of_birth', 'admission_date', 'admission_type', 'gender']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }
        labels = {
            'phone': 'Phone Number',
            'address': 'Residential Address',
            'father_name': 'Father\'s Name',
            'mother_name': 'Mother\'s Name',
            'parent_phone': 'Parent\'s Phone',
            'community': 'Community',
            'place_of_birth': 'Place of Birth',
            'admission_date': 'Admission Date',
            'admission_type': 'Admission Type',
            'gender': 'Gender',
        }

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'
            if not re.match(password_regex, new_password):
                raise forms.ValidationError(
                    "Password must be at least 12 characters long and contain at least one uppercase letter, "
                    "one lowercase letter, one number, and one special character (e.g., !@#$%)."
                )
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")
            if not self.cleaned_data.get("current_password"):
                raise forms.ValidationError("Current password is required to change the password.")
        return cleaned_data

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
    """Custom form to allow users to securely change their password on first login."""
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        min_length=12,
        help_text="Password must be at least 12 characters long and include one uppercase, one lowercase, one number, and one special character (e.g., !@#$%)."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'
        if not re.match(password_regex, new_password):
            raise forms.ValidationError(
                "Password must be at least 12 characters long and contain at least one uppercase letter, "
                "one lowercase letter, one number, and one special character (e.g., !@#$%)."
            )
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data