from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages

def role_selection(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if hasattr(request.user, 'student'):
            return redirect('students:student_dashboard')
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty:faculty_dashboard')
    return render(request, 'role_selection.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('role_selection')
    if request.user.is_superuser:
        return redirect('admin:index')
    return render(request, 'home.html', {
        'is_student': hasattr(request.user, 'student'),
        'is_faculty': hasattr(request.user, 'faculty'),
    })

def custom_logout(request):
    logout(request)
    return redirect('role_selection')

def accounts_profile_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        elif hasattr(request.user, 'student'):
            return redirect('students:student_profile')  
        elif hasattr(request.user, 'faculty'):
            return redirect('faculty:faculty_profile') 
    return redirect('role_selection')

class StudentLoginView(auth_views.LoginView):
    template_name = 'students/student_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('students:student_dashboard')  

class FacultyLoginView(auth_views.LoginView):
    template_name = 'faculty/faculty_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('faculty:faculty_dashboard') 

urlpatterns = [
    path('', role_selection, name='role_selection'),
    path('home/', home, name='home'),
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('admin/', admin.site.urls),
    path('student-login/', StudentLoginView.as_view(), name='student_login'),
    path('faculty-login/', FacultyLoginView.as_view(), name='faculty_login'),
    path('logout/', custom_logout, name='logout'),
    path('accounts/profile/', accounts_profile_redirect, name='accounts_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)