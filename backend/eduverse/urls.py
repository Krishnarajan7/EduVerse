from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.static import serve
from students.token_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to the EduVerse API",
        "endpoints": {
            "login": "/api/token/",
            "students": "/api/students/",
            "faculty": "/api/faculty/",
            "admin": "/admin/",
        },
    })

# Serve favicon.ico
def favicon(request):
    return serve(request, 'favicon.ico', document_root=settings.STATICFILES_DIRS[0])

urlpatterns = [
    path('', api_root, name='api_root'),
    path('favicon.ico', favicon, name='favicon'),
    path('admin/', admin.site.urls),
    path('api/students/', include('students.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)