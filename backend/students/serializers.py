from rest_framework import serializers
from .models import Student, Fee, Circular, ExamTimetable, ClassTimetable, Attendance
from faculty.models import Subject, Faculty
from students.models import Class

class StudentSerializer(serializers.ModelSerializer):
    class_group = serializers.StringRelatedField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'name', 'roll_number', 'phone', 'address',
            'email', 'changed_password', 'class_group'
        ]


class FeeSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()

    class Meta:
        model = Fee
        fields = ['id', 'student', 'amount', 'due_date', 'paid']


class CircularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circular
        fields = ['id', 'title', 'content', 'date_posted']


class ExamTimetableSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    class_group = serializers.StringRelatedField()

    class Meta:
        model = ExamTimetable
        fields = ['id', 'class_group', 'subject', 'date', 'time']


class ClassTimetableSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    class_group = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = ClassTimetable
        fields = ['id', 'class_group', 'subject', 'day', 'time', 'faculty']


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    class_group = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'status', 'student', 'subject', 'class_group', 'faculty']
