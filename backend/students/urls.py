from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('login/', views.StudentLoginView.as_view(), name='student_login'),
    path('profile/', views.student_profile, name='student_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('edit_profile/', views.edit_student_profile, name='edit_student_profile'),
    path('notice_calendar/', views.notice_calendar, name='notice_calendar'),
    path('master/', views.master, name='master'),
    path('admission/', views.admission, name='admission'),
    path('academic/', views.academic, name='academic'), 
    path('attendance/', views.attendance, name='attendance'),  
    path('circular/', views.circular, name='circular'),  
    path('exam_timetable/', views.exam_timetable, name='exam_timetable'),  
    path('class_timetable/', views.class_timetable, name='class_timetable'), 
    path('feedback/', views.feedback, name='feedback'),
    path('exam/', views.exam, name='exam'),
    path('fee/', views.fee, name='fee'),
    path('transport/', views.transport, name='transport'),
    path('placement/', views.placement, name='placement'),
]