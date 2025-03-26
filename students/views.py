from django.shortcuts import render
from .models import Student,Faculty

def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})

def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, "students/faculty_list.html", {"faculty": faculty})
