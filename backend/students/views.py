from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .models import Student, Attendance, Fee, Subject, Circular, ExamTimetable, ClassTimetable
from .forms import StudentProfileForm, ChangePasswordForm
from django.db.models import Sum, Avg
from datetime import datetime
import uuid

def role_selection(request):
    return render(request, 'students/role_selection.html')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/') 
        elif hasattr(request.user, 'student'):
            return redirect('students:student_dashboard')
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty:faculty_dashboard')
        else:
            return redirect('role_selection')
    return render(request, 'students/home.html', {'message': 'Please log in.'})

def custom_logout(request):
    logout(request)
    return redirect('home')

def accounts_profile_redirect(request):
    if hasattr(request.user, 'student'):
        return redirect('students:student_profile')
    elif hasattr(request.user, 'faculty'):
        return redirect('faculty:faculty_profile')
    return redirect('role_selection')

class StudentLoginView(View):
    def get(self, request):
        return render(request, 'students/student_login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'student'):
            login(request, user)
            student = user.student
            if not student.changed_password:
                return redirect('students:change_password')
            return redirect('students:student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
            return render(request, 'students/student_login.html')

class FacultyLoginView(View):
    def get(self, request):
        return render(request, 'faculty/faculty_login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'faculty'):
            login(request, user)
            return redirect('faculty:faculty_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a faculty.')
            return render(request, 'faculty/faculty_login.html')

@login_required
def student_profile(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            if current_password and not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return render(request, 'students/student_profile.html', {'form': form})
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                student.changed_password = True
                student.save()
                messages.success(request, 'Password updated successfully!')
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:student_profile')
    else:
        form = StudentProfileForm(instance=student)
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/student_profile.html', {
        'student': student,
        'form': form,
        'total_due': total_due,
        'attendance_percentage': student.attendance_percentage,
    })

@login_required
def change_password(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('students:change_password')
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                student.changed_password = True
                student.save()
                messages.success(request, 'Password updated successfully! Redirecting to dashboard.')
                return redirect('students:student_dashboard')
            else:
                messages.error(request, 'Passwords do not match.')
    else:
        form = ChangePasswordForm()
    return render(request, 'students/change_password.html', {'form': form})

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
    unpaid_fee = student.fees.filter(paid=False).first()
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    attendance_percentage = student.attendance_percentage
    average_marks = student.subjects.aggregate(avg=Avg('marks'))['avg'] or 0.00
    circulars = Circular.objects.all()[:5]
    exam_timetable = ExamTimetable.objects.all() 
    class_timetable = ClassTimetable.objects.all()
    can_edit_students = request.user.is_superuser or request.user.has_perm("students.change_student")

    return render(request, 'students/student_dashboard.html', {
        'student': student,
        'unpaid_fee': unpaid_fee,
        'total_due': total_due,
        'attendance_percentage': attendance_percentage,
        'average_marks': average_marks,
        'request': request,  
        'can_change_student': request.user.has_perm("students.change_student"),
        'circulars': circulars,
        'can_edit_students' : can_edit_students,
        'exam_timetable' : exam_timetable,
        'class_timetable' : class_timetable,
    })

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username.lower())
            student = user.student
            token = str(uuid.uuid4())
            student.reset_token = token
            student.reset_token_expiry = datetime.now() + datetime.timedelta(hours=24)
            student.save()
            reset_url = request.build_absolute_uri(reverse('students:reset_password', kwargs={'token': token}))
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                'from@example.com',
                [student.email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('students:login')
        except (User.DoesNotExist, Student.DoesNotExist):
            messages.error(request, 'Username not found.')
            return render(request, 'students/forgot_password.html')
    return render(request, 'students/forgot_password.html')

def reset_password(request, token):
    try:
        student = Student.objects.get(reset_token=token, reset_token_expiry__gt=datetime.now())
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password == confirm_password:
                student.user.set_password(new_password)
                student.user.save()
                student.changed_password = True
                student.reset_token = None
                student.reset_token_expiry = None
                student.save()
                messages.success(request, 'Password reset successfully. You can now log in.')
                return redirect('students:login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'students/reset_password.html', {'token': token})
    except Student.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('students:login')
    

    
@login_required
def academic(request):
    return redirect('students:student_dashboard')

@login_required
def edit_student_profile(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:student_profile')
    else:
        form = StudentProfileForm(instance=student)
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/edit_student_profile.html', {'form': form, 'total_due': total_due})

@login_required
def notice_calendar(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/notice_calendar.html', {'total_due': total_due})

@login_required
def master(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/master.html', {'student': student, 'total_due': total_due})

@login_required
def admission(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/admission.html', {'student': student, 'total_due': total_due})

@login_required
def academic(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    attendance_data = student.attendances.all()
    return render(request, 'students/academic.html', {'student': student, 'total_due': total_due, 'attendance_data': attendance_data})

@login_required
def feedback(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        messages.success(request, f'Feedback submitted: {feedback_text}')
        return redirect('students:feedback')
    return render(request, 'students/feedback.html', {'student': student, 'total_due': total_due})

@login_required
def exam(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/exam.html', {'student': student, 'total_due': total_due})

@login_required
def fee(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    fee_data = student.fees.all()
    return render(request, 'students/fee.html', {'student': student, 'total_due': total_due, 'fee_data': fee_data})

@login_required
def transport(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/transport.html', {'student': student, 'total_due': total_due})

@login_required
def placement(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return render(request, 'students/placement.html', {'student': student, 'total_due': total_due})


@login_required
def circular(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    circulars = Circular.objects.all()[:5] 
    return render(request, 'students/circular.html', {
        'circulars': circulars,
    })

@login_required
def exam_timetable(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    exam_timetable = ExamTimetable.objects.all()  
    return render(request, 'students/exam_timetable.html', {
        'exam_timetable': exam_timetable,
    })

@login_required
def class_timetable(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    class_timetable = ClassTimetable.objects.all()  
    return render(request, 'students/class_timetable.html', {
        'class_timetable': class_timetable,
    })
    
@login_required
def attendance(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    attendance_percentage = student.attendance_percentage
    return render(request, 'students/attendance.html', {
        'student': student,
        'attendance_percentage': attendance_percentage,
    })
