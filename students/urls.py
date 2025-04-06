from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/edit/', views.edit_student_profile, name='edit_student_profile'),
]