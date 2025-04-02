from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Class
from faculty.models import Notice, Resource

@login_required
def student_list(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class_id')
    students = Student.objects.all()
    if selected_class:
        students = students.filter(class_group_id=selected_class)
    return render(request, 'students/student_list.html', {'students': students, 'classes': classes})

@login_required
def student_profile(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    if request.method == 'POST':
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.save()
        from django.contrib import messages
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')
    return render(request, 'students/student_profile.html', {'student': student})

@login_required
def student_dashboard(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    notices = Notice.objects.all().order_by('-posted_at')[:5]
    resources = Resource.objects.filter(class_group=student.class_group).order_by('-uploaded_at')[:5]
    return render(request, 'students/student_dashboard.html', {
        'student': student,
        'notices': notices,
        'resources': resources,
    })