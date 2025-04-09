from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty, Resource, Notice
from .forms import StudentForm, AttendanceForm, MarksForm, ResourceForm, NoticeForm
from students.models import Student
from django.contrib import messages

@login_required
def faculty_list(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    faculty = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculty': faculty})

@login_required
def faculty_dashboard(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    faculty = request.user.faculty
    student_count = Student.objects.count()
    notices = Notice.objects.filter(posted_by=faculty).order_by('-posted_at')[:5]
    return render(request, 'faculty/faculty_dashboard.html', {
        'faculty': faculty,
        'student_count': student_count,
        'notices': notices,
    })

@login_required
def add_student(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
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
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
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
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'faculty/delete_student.html', {'student': student})

@login_required
def manage_attendance(request, student_id):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully!')
            return redirect('student_list')
    else:
        form = AttendanceForm(instance=student)
    return render(request, 'faculty/manage_attendance.html', {'form': form, 'student': student})

@login_required
def add_marks(request, student_id):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.save()
            messages.success(request, 'Marks added successfully!')
            return redirect('student_list')
    else:
        form = MarksForm()
    return render(request, 'faculty/add_marks.html', {'form': form, 'student': student})

@login_required
def upload_resource(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user.faculty
            resource.save()
            messages.success(request, 'Resource uploaded successfully!')
            return redirect('faculty_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'faculty/upload_resource.html', {'form': form})

@login_required
def post_notice(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user.faculty
            notice.save()
            messages.success(request, 'Notice posted successfully!')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'faculty/post_notice.html', {'form': form})

@login_required
def edit_notice(request, notice_id):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'faculty/edit_notice.html', {'form': form, 'notice': notice})

@login_required
def delete_notice(request, notice_id):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')
    return render(request, 'faculty/delete_notice.html', {'notice': notice})

@login_required
def notice_list(request):
    if request.user.is_superuser:
        return redirect('role_selection')
    notices = Notice.objects.all().order_by('-posted_at')
    return render(request, 'faculty/notice_list.html', {'notices': notices})


@login_required
def notice_calendar(request):
    if request.user.is_superuser or not hasattr(request.user, 'faculty'):
        return redirect('role_selection')
    faculty = request.user.faculty
    notices = Notice.objects.all().order_by('-posted_at')
    return render(request, 'faculty/notice_calendar.html', {'faculty': faculty, 'notices': notices})