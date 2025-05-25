from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, Avg
from .models import Student, Attendance, Fee, Subject, Circular, ExamTimetable, ClassTimetable
from .serializers import (
    StudentSerializer, FeeSerializer, CircularSerializer,
    ExamTimetableSerializer, ClassTimetableSerializer, AttendanceSerializer
)
from django.contrib.auth.models import User
import uuid
from datetime import timedelta

# -------------------- Helper Function --------------------
def get_student_data(student):
    """Helper function to fetch common student data for multiple views."""
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return {
        "student": StudentSerializer(student).data,
        "total_due": total_due,
    }

# -------------------- General Views --------------------
@api_view(['GET'])
def role_selection(request):
    return Response({"message": "Role selection is handled by the frontend."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request):
    if not request.user.is_authenticated:
        return Response({"message": "Please log in."}, status=status.HTTP_200_OK)
    if request.user.is_superuser:
        return Response({"redirect": "/admin/"}, status=status.HTTP_302_FOUND)
    elif hasattr(request.user, 'student'):
        return Response({"redirect": "/api/students/dashboard/"}, status=status.HTTP_302_FOUND)
    elif hasattr(request.user, 'faculty'):
        return Response({"redirect": "/api/faculty/dashboard/"}, status=status.HTTP_302_FOUND)
    return Response({"redirect": "/role-selection"}, status=status.HTTP_302_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    if request.user.is_superuser:
        return Response({"role": "admin"}, status=status.HTTP_200_OK)
    elif hasattr(request.user, 'student'):
        return Response({"role": "student"}, status=status.HTTP_200_OK)
    elif hasattr(request.user, 'faculty'):
        return Response({"role": "faculty"}, status=status.HTTP_200_OK)
    return Response({"role": "unknown"}, status=status.HTTP_200_OK)

# -------------------- StudentViewSet --------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter']
    filterset_fields = ['class_name', 'section']
    search_fields = ['name', 'roll_number']
    pagination_class = 'rest_framework.pagination.PageNumberPagination'

# -------------------- Login Views --------------------
# Note: Login/logout are handled by SimpleJWT endpoints (/api/token/, /api/token/blacklist/)
# These views are adjusted to work with JWT-based authentication.

@api_view(['GET'])
def student_login(request):
    return Response({"message": "Login page is handled by the frontend. Use /api/token/ for authentication."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def faculty_login(request):
    return Response({"message": "Login page is handled by the frontend. Use /api/token/ for authentication."}, status=status.HTTP_200_OK)

# -------------------- Student Dashboard --------------------
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

# -------------------- Profile & Password --------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

    student = request.user.student
    if request.method == 'POST':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    serializer = StudentSerializer(student)
    total_due = student.fees.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0.00
    return Response({
        "student": serializer.data,
        "total_due": total_due,
        "attendance_percentage": student.attendance_percentage,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

    student = request.user.student
    if 'profile_picture' not in request.FILES:
        return Response({"error": "No profile picture provided."}, status=status.HTTP_400_BAD_REQUEST)

    student.profile_picture = request.FILES['profile_picture']
    student.save()
    serializer = StudentSerializer(student)
    return Response({"message": "Profile picture uploaded successfully!", "student": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

    student = request.user.student
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not all([current_password, new_password, confirm_password]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not request.user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.save()
    student.changed_password = True
    student.save()
    return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)

# -------------------- Forgot/Reset Password --------------------
@api_view(['POST', 'GET'])
def forgot_password(request):
    if request.method == 'POST':
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username.lower())
            student = user.student
            token = str(uuid.uuid4())
            student.reset_token = token
            student.reset_token_expiry = timezone.now() + timedelta(hours=24)
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
        student = Student.objects.get(reset_token=token, reset_token_expiry__gt=timezone.now())
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

# -------------------- Other Student Features --------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def edit_student_profile(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

    student = request.user.student
    if request.method == 'POST':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response(get_student_data(student), status=status.HTTP_200_OK)

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
    return Response(get_student_data(request.user.student), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admission(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(get_student_data(request.user.student), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def academic(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    student = request.user.student
    attendance_data = student.attendances.all()
    data = get_student_data(student)
    data["attendance_data"] = AttendanceSerializer(attendance_data, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def feedback(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    student = request.user.student
    if request.method == 'POST':
        feedback_text = request.data.get('feedback')
        return Response({"message": f"Feedback submitted: {feedback_text}"}, status=status.HTTP_200_OK)
    return Response(get_student_data(student), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(get_student_data(request.user.student), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fee(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    student = request.user.student
    fee_data = student.fees.all()
    data = get_student_data(student)
    data["fee_data"] = FeeSerializer(fee_data, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transport(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(get_student_data(request.user.student), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placement(request):
    if not hasattr(request.user, 'student'):
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(get_student_data(request.user.student), status=status.HTTP_200_OK)

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
    return Response({
        "student": StudentSerializer(student).data,
        "attendance_percentage": student.attendance_percentage,
    }, status=status.HTTP_200_OK)