from django.urls import path, include

urlpatterns = [
    path('students/', include('students.urls')),
]