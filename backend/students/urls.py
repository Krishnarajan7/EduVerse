from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('role-selection/', views.role_selection, name='role_selection'),
    path('', views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/profile/', views.accounts_profile_redirect, name='accounts_profile'),
    path('login/', views.student_login, name='login'),
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('profile/', views.student_profile, name='student_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('edit-profile/', views.edit_student_profile, name='edit_student_profile'),
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