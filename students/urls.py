from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('profile/', views.student_profile, name='student_profile'),
]