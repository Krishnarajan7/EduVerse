from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib import messages
from .models import Student, Class
from faculty.models import Notice, Resource
from .forms import StudentProfileForm, ChangePasswordForm
from django.db.models import Sum, Avg

def is_admin_or_faculty(user):
    return user.is_superuser or hasattr(user, 'faculty')

@login_required
@user_passes_test(is_admin_or_faculty, login_url='student_profile')
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
    
    # Precompute attendance summary
    total_attendances = student.attendances.count()
    present_count = student.attendances.filter(is_present=True).count()
    attendance_percentage = (present_count / total_attendances * 100 if total_attendances > 0 else 0)
    
    # Precompute fee summary
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    
    # Precompute average marks
    average_marks = student.subjects.aggregate(avg=Avg('marks'))['avg'] or 0.00
    
    # Fetch notices and resources
    notices = Notice.objects.all().order_by('-posted_at')[:5].select_related('posted_by')
    resources = Resource.objects.filter(class_group=student.class_group).order_by('-uploaded_at')[:5].select_related('uploaded_by')

    return render(request, 'students/student_profile.html', {
        'student': student,
        'total_attendances': total_attendances,
        'present_count': present_count,
        'attendance_percentage': attendance_percentage,
        'total_due': total_due,
        'average_marks': average_marks,
        'notices': notices,
        'resources': resources,
    })

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

    if not student.changed_password:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']

                if request.user.check_password(current_password):
                    request.user.set_password(new_password)
                    request.user.save()

                    student.changed_password = True
                    student.save()

                    user = authenticate(request, username=request.user.username, password=new_password)
                    if user is not None:
                        login(request, user)
                        update_session_auth_hash(request, user) 
                        messages.success(request, 'Password changed successfully.')
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, 'Authentication failed after password change.')
                else:
                    messages.error(request, 'Current password is incorrect.')
        else:
            form = ChangePasswordForm()
        return render(request, 'students/change_password.html', {'form': form})

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
                return redirect('student_dashboard')  
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'students/student_login.html')

@login_required
def notice_calendar(request):
    if request.user.is_superuser or not hasattr(request.user, 'student'):
        return redirect('role_selection')
    return render(request, 'students/notice_calendar.html')