from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Faculty, Resource, Notice, FacultyIncharge, FacultyPeriodAssignment
from .forms import StudentForm, AttendanceForm, MarksForm, ResourceForm, NoticeForm
from students.models import Student

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed successfully.')
        return redirect('faculty_dashboard')

@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')  
    faculty = request.user.faculty
    context = {'faculty': faculty}
    
    incharge = getattr(faculty, 'incharge_role', None)
    if incharge:
        context.update({
            'student_count': Student.objects.filter(class_group=incharge.class_group).count(),
            'notices': Notice.objects.filter(posted_by=faculty, class_group=incharge.class_group).order_by('-posted_at')[:5],
            'class_group': incharge.class_group
        })
    
    return render(request, 'faculty/faculty_dashboard.html', context)

@login_required
def student_list(request):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    
    if not incharge:
        messages.error(request, 'You are not a class incharge.')
        return redirect('faculty_dashboard')
    
    students = Student.objects.filter(class_group=incharge.class_group)
    return render(request, 'faculty/student_list.html', {'students': students})

@login_required
def add_student(request):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    
    if not incharge:
        messages.error(request, 'You are not authorized to add students.')
        return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['class_group'] != incharge.class_group:
                messages.error(request, "You can only add students to your assigned class.")
                return redirect('add_student')
            from django.contrib.auth.models import User
            username = form.cleaned_data['roll_number'].lower()
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password='password123')
            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(initial={'class_group': incharge.class_group})
    return render(request, 'faculty/add_student.html', {'form': form})


@login_required
def update_student(request, student_id):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    if not incharge:
        messages.error(request, 'You are not authorized to update students.')
        return redirect('student_list')
    student = get_object_or_404(Student, id=student_id)
    if student.class_group != incharge.class_group:
        messages.error(request, "You are not authorized to update this student.")
        return redirect('student_list')
    

@login_required
def delete_student(request, student_id):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    if not incharge:
        messages.error(request, 'You are not authorized to delete students.')
        return redirect('student_list')
    student = get_object_or_404(Student, id=student_id)
    if student.class_group != incharge.class_group:
        messages.error(request, "You are not authorized to delete this student.")
        return redirect('student_list')
    

@login_required
def manage_attendance(request, student_id):
    faculty = request.user.faculty
    
    assignment = FacultyPeriodAssignment.objects.filter(faculty=faculty).first()
    if not assignment:
        messages.error(request, 'You are not authorized to manage attendance.')
        return redirect('faculty_dashboard')
    student = get_object_or_404(Student, id=student_id)
    if student.class_group != assignment.class_group:
        messages.error(request, "You are not assigned to this student's class.")
        return redirect('student_list')


@login_required
def add_marks(request, student_id):
    faculty = request.user.faculty
    assignment = FacultyPeriodAssignment.objects.filter(faculty=faculty).first()
    if not assignment:
        messages.error(request, 'You are not authorized to add marks.')
        return redirect('student_list')
    student = get_object_or_404(Student, id=student_id)
    if student.class_group != assignment.class_group:
        messages.error(request, "You are not authorized to add marks for this student.")
        return redirect('student_list')
    

@login_required
def upload_resource(request):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    if not incharge:
        messages.error(request, 'You are not authorized to upload resources.')
        return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = faculty
            resource.class_group = incharge.class_group
            resource.save()
            messages.success(request, 'Resource uploaded successfully!')
            return redirect('faculty_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'faculty/upload_resource.html', {'form': form})

@login_required
def post_notice(request):
    faculty = request.user.faculty
    incharge = getattr(faculty, 'incharge_role', None)
    if not incharge:
        messages.error(request, 'You are not authorized to post notices.')
        return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = faculty
            notice.class_group = incharge.class_group
            notice.save()
            messages.success(request, 'Notice posted successfully!')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'faculty/post_notice.html', {'form': form})

@login_required
def edit_notice(request, notice_id):
    faculty = getattr(request.user, 'faculty', None)
    if not faculty:
        return redirect('role_selection')

    notice = get_object_or_404(Notice, id=notice_id)
    if notice.posted_by != faculty:
        messages.error(request, 'You are not authorized to edit this notice.')
        return redirect('notice_list')

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
    faculty = getattr(request.user, 'faculty', None)
    if not faculty:
        return redirect('role_selection')

    notice = get_object_or_404(Notice, id=notice_id)
    if notice.posted_by != faculty:
        messages.error(request, 'You are not authorized to delete this notice.')
        return redirect('notice_list')

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
