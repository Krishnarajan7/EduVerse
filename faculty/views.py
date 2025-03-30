from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty
from .forms import StudentForm
from students.models import Student
from django.contrib import messages

@login_required
def faculty_list(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('home')
    faculty = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculty': faculty})

@login_required
def add_student(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('home')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            from django.contrib.auth.models import User
            username = form.cleaned_data['roll_number'].lower()
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password='password123')
            student.user = user
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'faculty/add_student.html', {'form': form})

@login_required
def update_student(request, student_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('home')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'faculty/update_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, student_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('home')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete() 
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'faculty/delete_student.html', {'student': student})