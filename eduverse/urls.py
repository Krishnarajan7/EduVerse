from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]