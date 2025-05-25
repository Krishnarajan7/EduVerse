from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Student
from .serializers import StudentSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        student = Student.objects.get(user=self.user)
        data['student'] = {
            'id': student.id,
            'name': student.name,
            'roll_number': student.roll_number,
            'class_name': student.class_name,
            'section': student.section,
        }
        return data