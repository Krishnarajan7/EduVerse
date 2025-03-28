from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Class
from .forms import StudentProfileForm
from django.contrib import messages

def student_list(request):
    classes = Class.objects.all()
    selected_class_id = request.GET.get('class_id')
    if selected_class_id:
        students = Student.objects.filter(class_group__id=selected_class_id)
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students, 'classes': classes})

@login_required
def student_profile(request):
    if not hasattr(request.user, 'student'):
        return redirect('home')
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'students/student_profile.html', {'student': student, 'form': form})