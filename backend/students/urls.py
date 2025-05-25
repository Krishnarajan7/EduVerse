from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')

app_name = 'students'
urlpatterns = [
    path('', include(router.urls)),
    path('user-role/', views.get_user_role, name='get_user_role'),
    path('profile/', views.student_profile, name='student_profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('notice-calendar/', views.notice_calendar, name='notice_calendar'),
    path('master/', views.master, name='master'),
    path('admission/', views.admission, name='admission'),
    path('academic/', views.academic, name='academic'),
    path('feedback/', views.feedback, name='feedback'),
    path('exam/', views.exam, name='exam'),
    path('fee/', views.fee, name='fee'),
    path('transport/', views.transport, name='transport'),
    path('placement/', views.placement, name='placement'),
    path('circular/', views.circular, name='circular'),
    path('exam-timetable/', views.exam_timetable, name='exam_timetable'),
    path('class-timetable/', views.class_timetable, name='class_timetable'),
    path('attendance/', views.attendance, name='attendance'),
]