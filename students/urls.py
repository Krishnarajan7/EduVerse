from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('profile/', views.student_profile, name='student_profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
]