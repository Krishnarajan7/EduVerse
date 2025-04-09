from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('profile/', views.student_profile, name='student_profile'),
    path('edit-profile/', views.edit_student_profile, name='edit_student_profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.student_login_view, name='student_login'),
    path('notice-calendar/', views.notice_calendar, name='notice_calendar'),  # Add this line
]