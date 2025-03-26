from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to EduVerse ERP!")

urlpatterns = [
    path('', home, name='home'), 
    path('students/', include('students.urls')),
    path('admin/', admin.site.urls),
]