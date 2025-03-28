from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'), 
    path('students/', include('students.urls')),
    path('faculty/',include('faculty.urls')),
    path('admin/', admin.site.urls),
]