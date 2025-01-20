from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegisterSerializer, VerifySmsCodeSerializer, LoginSerializer, StudentProfileSerializer
from .models import Student
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.shortcuts import get_object_or_404



class StudentProfileAPIView(APIView):

    def get(self, request, *args, **kwargs):
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        token = token_header.split(' ')[1]

        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=status.HTTP_401_UNAUTHORIZED)

   
        student_id = decoded_token.get('student_id')
      
        if not student_id:
            raise AuthenticationFailed('Student ID not found in token')


        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)
        data = {
            "full_name": student.full_name,
            "email": student.user.email,  # Student bilan bog'liq foydalanuvchi
            "phone": student.user.phone,  # Telefon raqam foydalanuvchining username sifatida saqlangan
            "region": student.region,
            "districts": student.districts,
            "address": student.address,
            "brithday": student.brithday,
            "academy_or_school": student.academy_or_school,
            "class_name": student.class_name,
        }

        return Response(data)
















class RegisterStudentAPIView(APIView):
    """
    API to register user and send SMS code.
    """
    def post(self, request, *args, **kwargs):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Telefon raqamga SMS kodi yuborildi. Kodni tasdiqlang."}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifySmsCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

            # Generate JWT token with custom claims
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(hours=3))
            access_token['student_id'] = student.id   # Token expires in 3 hours
            expires_in = timedelta(hours=3).total_seconds()

            return Response({
                "message": "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.",
                "login": serializer.validated_data['phone'],
                "password": serializer.validated_data['password'],
                "access_token": str(access_token),  # Return the token as string
                "expires_in": expires_in,  # Include the expiration time in seconds
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

            # Generate JWT token with custom claims
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(hours=3))  # Set expiration to 1 minute
            access_token['student_id'] = student.id  # Add student ID to the token payload

       
            expires_in = timedelta(hours=3).total_seconds()  # 1 minute = 60 seconds

            student_data = {
                "id": student.id,
                "full_name": student.full_name,
                "email": user.email,
                "phone": user.phone,
                "region": student.region,
                "districts": student.districts,
                "address": student.address,
                "brithday": student.brithday,
                "academy_or_school": student.academy_or_school,
                "class_name": student.class_name,
                "status": student.status,
                "access_token": str(access_token),  # Return the token as string
                "expires_in": expires_in,  # Include the expiration time in seconds
            }
            
            return Response(student_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
