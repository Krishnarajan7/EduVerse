from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, logout
from django.conf import settings
from django.conf.urls.static import static

def role_selection(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if hasattr(request.user, 'student'):
            return redirect('student_dashboard')
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty_dashboard')
        else:
            # If user has no profile, log them out and show role selection
            logout(request)
            return render(request, 'role_selection.html')
    return render(request, 'role_selection.html')

def home(request):
    if not request.user.is_authenticated or request.user.is_superuser:
        return redirect('role_selection')
    if hasattr(request.user, 'student'):
        return redirect('student_dashboard')
    elif hasattr(request.user, 'faculty'):
        return redirect('faculty_dashboard')
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('role_selection')

urlpatterns = [
    path('', role_selection, name='role_selection'),
    path('home/', home, name='home'),
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('admin/', admin.site.urls),
    path('student-login/', auth_views.LoginView.as_view(
        template_name='students/student_login.html',
        redirect_authenticated_user=True,
        extra_context={'next': '/students/dashboard/'}
    ), name='student_login'),
    path('faculty-login/', auth_views.LoginView.as_view(
        template_name='faculty/faculty_login.html',
        redirect_authenticated_user=True,
        extra_context={'next': '/faculty/dashboard/'}
    ), name='faculty_login'),
    path('logout/', custom_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)