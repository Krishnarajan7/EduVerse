from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentForm, AttendanceForm, MarksForm, ResourceForm, NoticeForm, FacultyForm
from students.models import Student, Class, Subject
from .models import Notice, Resource, Faculty
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def faculty_dashboard(request):
    return render(request, 'faculty/faculty_dashboard.html')

@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculties': faculties})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'faculty/student_list.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'faculty/add_student.html', {'form': form})

@login_required
def update_student(request, student_id):
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
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'faculty/delete_student.html', {'student': student})

@login_required
def manage_attendance(request, student_id):
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
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.student = student
            subject.save()
            messages.success(request, 'Marks added successfully!')
            return redirect('student_list')
    else:
        form = MarksForm()
    return render(request, 'faculty/add_marks.html', {'form': form, 'student': student})

@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource uploaded successfully!')
            return redirect('faculty_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'faculty/upload_resource.html', {'form': form})

@login_required
def post_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice posted successfully!')
            return redirect('faculty_dashboard')
    else:
        form = NoticeForm()
    return render(request, 'faculty/post_notice.html', {'form': form})

@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'faculty/notice_list.html', {'notices': notices})

@login_required
def edit_notice(request, notice_id):
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
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')
    return render(request, 'faculty/delete_notice.html', {'notice': notice})

@login_required
def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty added successfully!')
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'faculty/add_faculty.html', {'form': form})

@login_required
def notice_calendar(request):
    notices = Notice.objects.all()
    return render(request, 'faculty/notice_calendar.html', {'notices': notices})

@login_required
def notice_events(request):
    notices = Notice.objects.all()
    events = [
        {
            'title': notice.title,
            'start': notice.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': notice.content,
        }
        for notice in notices
    ]
    return JsonResponse(events, safe=False)