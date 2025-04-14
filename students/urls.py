from django.urls import path
from . import views

app_name = 'students'  

urlpatterns = [
    path('login/', views.StudentLoginView.as_view(), name='student_login'),
    path('profile/', views.student_profile, name='student_profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('edit_profile/', views.edit_student_profile, name='edit_student_profile'),
    path('notice_calendar/', views.notice_calendar, name='notice_calendar'),
    path('master/', views.master, name='master'),
    path('admission/', views.admission, name='admission'),  
    path('academic/', views.academic, name='academic'),
    path('feedback/', views.feedback, name='feedback'),
    path('exam/', views.exam, name='exam'),
    path('fee/', views.fee, name='fee'),
    path('transport/', views.transport, name='transport'),
    path('placement/', views.placement, name='placement'),
]