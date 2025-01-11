from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegisterSerializer, VerifySmsCodeSerializer, LoginSerializer
from .models import Student
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
            return Response({
                "message": "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.",
                "login": serializer.validated_data['phone'],
                "password": serializer.validated_data['password']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            # Retrieve the Student profile associated with the User
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

            # Return the details of the Student
            student_data = {
                "full_name": student.full_name,
                "email": user.email,
                "phone": user.phone,
                "region": student.region.name,  # Assuming 'region' is a related model
                "districts": student.districts.name,  # Assuming 'districts' is a related model
                "address": student.address,
                "brithday": student.brithday,
                "academy_or_school": student.academy_or_school,
                "class_name": student.class_name,
                "status": student.status
            }
            
            return Response(student_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)