from rest_framework import serializers
from .models import Student, Fee, Circular, ExamTimetable, ClassTimetable, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'phone', 'address', 'email', 'changed_password']

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ['id', 'amount', 'due_date', 'paid']

class CircularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circular
        fields = ['id', 'title', 'content', 'date_posted']

class ExamTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTimetable
        fields = ['id', 'subject', 'date', 'time']

class ClassTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTimetable
        fields = ['id', 'subject', 'day', 'time']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'status']