from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib import messages
from .models import Student, Class
from faculty.models import Notice, Resource
from .forms import StudentProfileForm, ChangePasswordForm


@login_required
def student_list(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class_id')
    students = Student.objects.all().select_related('user')
    if selected_class:
        students = students.filter(class_group_id=selected_class)
    return render(request, 'students/student_list.html', {'students': students, 'classes': classes})


@login_required
def student_profile(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    if request.method == 'POST':
        student.phone = request.POST.get('phone', student.phone)
        student.address = request.POST.get('address', student.address)
        student.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')
    return render(request, 'students/student_profile.html', {'student': student})


@login_required
def edit_student_profile(request):
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'students/edit_student_profile.html', {'form': form})


@login_required
def student_dashboard(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')

    student = request.user.student

    # If the password hasn't been changed yet
    if not student.changed_password:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']

                if request.user.check_password(current_password):
                    # Change the password
                    request.user.set_password(new_password)
                    request.user.save()

                    # Mark password as changed
                    student.changed_password = True
                    student.save()

                    # Keep user logged in after password change
                    user = authenticate(request, username=request.user.username, password=new_password)
                    if user is not None:
                        login(request, user)
                        update_session_auth_hash(request, user)  # super important
                        messages.success(request, 'Password changed successfully.')
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, 'Authentication failed after password change.')
                else:
                    messages.error(request, 'Current password is incorrect.')
        else:
            form = ChangePasswordForm()
        return render(request, 'students/change_password.html', {'form': form})

    # If password is already changed, show dashboard
    notices = Notice.objects.all().order_by('-posted_at')[:5].select_related('posted_by')
    resources = Resource.objects.filter(class_group=student.class_group).order_by('-uploaded_at')[:5].select_related('uploaded_by')

    return render(request, 'students/student_dashboard.html', {
        'student': student,
        'notices': notices,
        'resources': resources,
    })



def student_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'student'):
            login(request, user)
            student = user.student
            if not student.changed_password:
                return redirect('student_dashboard')  # Will redirect to password change
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'students/student_login.html')


@login_required
def notice_calendar(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')
    return render(request, 'students/notice_calendar.html')
