from django.shortcuts import render
from .models import Faculty

def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, "faculty/faculty_list.html", {"faculty": faculty})


