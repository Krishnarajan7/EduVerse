from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

def role_selection(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            return redirect('student_dashboard')
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty_dashboard')
    return render(request, 'role_selection.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('role_selection')
    if hasattr(request.user, 'student'):
        return redirect('student_dashboard')
    elif hasattr(request.user, 'faculty'):
        return redirect('faculty_dashboard')
    return render(request, 'home.html')

urlpatterns = [
    path('', role_selection, name='role_selection'),
    path('home/', home, name='home'),
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('admin/', admin.site.urls),
    path('student-login/', auth_views.LoginView.as_view(template_name='students/student_login.html', redirect_authenticated_user=True), name='student_login'),
    path('faculty-login/', auth_views.LoginView.as_view(template_name='faculty/faculty_login.html', redirect_authenticated_user=True), name='faculty_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='role_selection'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)