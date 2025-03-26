from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name = 'student_list'),
    path('faculty/',views.faculty_list, name = 'faculty_list')
]