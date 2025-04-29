from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .models import Student, Attendance, Fee, Subject, Circular, ExamTimetable, ClassTimetable
from .forms import StudentProfileForm, ChangePasswordForm
from .serializers import StudentSerializer, FeeSerializer, CircularSerializer, ExamTimetableSerializer, ClassTimetableSerializer, AttendanceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Avg
from datetime import datetime
import uuid

@api_view(['GET'])
def role_selection(request):
    # Since this is a UI route, redirect to frontend or return a simple message
    return Response({"message": "Role selection is handled by the frontend."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return Response({"redirect": "/admin/"}, status=status.HTTP_302_FOUND)
        elif hasattr(request.user, 'student'):
            return Response({"redirect": "/api/students/dashboard/"}, status=status.HTTP_302_FOUND)
        elif hasattr(request.user, 'faculty'):
            return Response({"redirect": "/api/faculty/dashboard/"}, status=status.HTTP_302_FOUND)
        else:
            return Response({"redirect": "/role-selection"}, status=status.HTTP_302_FOUND)
    return Response({"message": "Please log in."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def custom_logout(request):
    logout(request)
    return Response({"message": "Logged out successfully", "redirect": "/"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts_profile_redirect(request):
    if hasattr(request.user, 'student'):
        return Response({"redirect": "/api/students/profile/"}, status=status.HTTP_302_FOUND)
    elif hasattr(request.user, 'faculty'):
        return Response({"redirect": "/api/faculty/profile/"}, status=status.HTTP_302_FOUND)
    return Response({"redirect": "/role-selection"}, status=status.HTTP_302_FOUND)

@api_view(['POST', 'GET'])
def student_login(request):
    if request.method == 'GET':
        return Response({"message": "Login page is handled by the frontend."}, status=status.HTTP_200_OK)
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and hasattr(user, 'student'):
        login(request, user)
        student = user.student
        if not student.changed_password:
            return Response({"redirect": "/api/students/change-password/"}, status=status.HTTP_302_FOUND)
        return Response({"message": "Login successful", "redirect": "/api/students/dashboard/"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials or not a student."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST', 'GET'])
def faculty_login(request):
    if request.method == 'GET':
        return Response({"message": "Login page is handled by the frontend."}, status=status.HTTP_200_OK)
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and hasattr(user, 'faculty'):
        login(request, user)
        return Response({"message": "Login successful", "redirect": "/api/faculty/dashboard/"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials or not a faculty."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.data, request.FILES, instance=student)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            if current_password and not request.user.check_password(current_password):
                return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                student.changed_password = True
                student.save()
            form.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid form data.", "details": form.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = StudentSerializer(student)
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": serializer.data,
        "total_due": total_due,
        "attendance_percentage": student.attendance_percentage,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    form = ChangePasswordForm(request.data)
    if form.is_valid():
        current_password = form.cleaned_data['current_password']
        if not request.user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']
        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            student.changed_password = True
            student.save()
            return Response({"message": "Password updated successfully!", "redirect": "/api/students/dashboard/"}, status=status.HTTP_200_OK)
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Invalid form data.", "details": form.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    unpaid_fee = student.fees.filter(paid=False).first()
    attendance_percentage = student.attendance_percentage
    average_marks = student.subjects.aggregate(avg=Avg('marks'))['avg'] or 0.00
    circulars = Circular.objects.all()[:5]
    exam_timetable = ExamTimetable.objects.all()
    class_timetable = ClassTimetable.objects.all()

    return Response({
        "student": StudentSerializer(student).data,
        "unpaid_fee": FeeSerializer(unpaid_fee).data if unpaid_fee else None,
        "total_due": total_due,
        "attendance_percentage": attendance_percentage,
        "average_marks": average_marks,
        "circulars": CircularSerializer(circulars, many=True).data,
        "exam_timetable": ExamTimetableSerializer(exam_timetable, many=True).data,
        "class_timetable": ClassTimetableSerializer(class_timetable, many=True).data,
        "can_edit_students": request.user.is_superuser or request.user.has_perm("students.change_student"),
    }, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def forgot_password(request):
    if request.method == 'POST':
        username = request.data.get('username')
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
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Student.DoesNotExist):
            return Response({"error": "Username not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Forgot password page is handled by the frontend."}, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def reset_password(request, token):
    try:
        student = Student.objects.get(reset_token=token, reset_token_expiry__gt=datetime.now())
        if request.method == 'POST':
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if new_password == confirm_password:
                student.user.set_password(new_password)
                student.user.save()
                student.changed_password = True
                student.reset_token = None
                student.reset_token_expiry = None
                student.save()
                return Response({"message": "Password reset successfully. You can now log in."}, status=status.HTTP_200_OK)
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Reset password page is handled by the frontend.", "token": token}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edit_student_profile(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    if request.method == 'POST':
        form = StudentProfileForm(request.data, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid form data.", "details": form.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notice_calendar(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    total_due = request.user.student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({"total_due": total_due}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def master(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admission(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def academic(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    attendance_data = student.attendances.all()
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
        "attendance_data": AttendanceSerializer(attendance_data, many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def feedback(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    if request.method == 'POST':
        feedback_text = request.data.get('feedback')
        return Response({"message": f"Feedback submitted: {feedback_text}"}, status=status.HTTP_200_OK)
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fee(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    fee_data = student.fees.all()
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
        "fee_data": FeeSerializer(fee_data, many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transport(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placement(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def circular(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    circulars = Circular.objects.all()[:5]
    return Response({
        "circulars": CircularSerializer(circulars, many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_timetable(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    exam_timetable = ExamTimetable.objects.all()
    return Response({
        "exam_timetable": ExamTimetableSerializer(exam_timetable, many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def class_timetable(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    class_timetable = ClassTimetable.objects.all()
    return Response({
        "class_timetable": ClassTimetableSerializer(class_timetable, many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user.student
    attendance_percentage = student.attendance_percentage
    return Response({
        "student": StudentSerializer(student).data,
        "attendance_percentage": attendance_percentage,
    }, status=status.HTTP_200_OK)