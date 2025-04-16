from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from .models import Student, Attendance, Fee
from .forms import StudentProfileForm
from django.db.models import Sum, Avg
from datetime import datetime

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
                return redirect('students:student_dashboard') 
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
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('role_selection')
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    attendance_percentage = student.attendance_percentage
    average_marks = student.subjects.aggregate(avg=Avg('marks'))['avg'] or 0.00
    return render(request, 'students/student_dashboard.html', {
        'student': student,
        'total_due': total_due,
        'attendance_percentage': attendance_percentage,
        'average_marks': average_marks,
        'request': request,  
    })

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