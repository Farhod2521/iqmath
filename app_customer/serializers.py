from rest_framework import serializers
from .models import User, Student
import random
from .sms_service import send_sms  # SMS sending function
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()




class StudentProfileSerializer(serializers.Serializer):
    class Meta:
        model  =  Student
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        # Try to authenticate the user with phone and password
        user = authenticate(phone=phone, password=password)

        if user is None:
            raise serializers.ValidationError("Telefon raqam yoki parol noto'g'ri.")
        
        # Return user data for the next step (e.g., passing to the view)
        return {
            "user": user
        }

class StudentRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    region = serializers.CharField(required=True)  # This will be the ID of the Region
    districts = serializers.CharField(required=True)  # This will be the ID of the districts
    address = serializers.CharField(required=True)
    brithday = serializers.CharField(required=True)
    academy_or_school = serializers.CharField(required=True)
    class_name = serializers.CharField(required=True)

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        return value

    def create(self, validated_data):
        # Remove non-User fields (these will be saved in the Student model)
        student_data = {
            'full_name': validated_data.pop('full_name'),
            'address': validated_data.pop('address'),
            'brithday': validated_data.pop('brithday'),
            'academy_or_school': validated_data.pop('academy_or_school'),
            'class_name': validated_data.pop('class_name'),
            "region": validated_data.pop('region'),
            "districts": validated_data.pop('districts'),
        }



        # Create user
        phone = validated_data.pop('phone')
        user = User.objects.create(phone=phone, email=validated_data['email'], role='student')

        # Generate SMS code
        #sms_code = str(random.randint(10000, 99999))  # 6-digit code
        sms_code = str(12345)  # 5-digit code
        user.sms_code = sms_code
        user.set_unusable_password()  # Password is not set yet
        user.save()
        print(sms_code)

        # Create student profile with the Region and districts instances
        student_data['user'] = user

        student = Student.objects.create(**student_data)

        # Send SMS with the code
        #send_sms(phone, message=f"Bu Eskiz dan test")

        return user  # Return the user object after creation

import random
import string

class VerifySmsCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    sms_code = serializers.CharField(required=True)

    def validate(self, data):
        phone = data.get('phone')
        sms_code = data.get('sms_code')

        try:
            user = User.objects.get(phone=phone, sms_code=sms_code)
        except User.DoesNotExist:
            raise serializers.ValidationError("Telefon raqam yoki kod noto'g'ri.")

        # Custom password generation with letters, numbers, and symbols
        chars = string.ascii_letters + string.digits + '@#$'
        password = ''.join(random.choice(chars) for _ in range(8))

        # Set the password for the user
        user.set_password(password)
        user.sms_code = None  # Clear the SMS code
        user.save()

        # Update student status to True
        student = Student.objects.get(user=user)
        student.status = True  # Set the student status to True
        student.save()
        print(f"Sizning login: {user.phone} va parolingiz: {password}")
        # Send LOGIN and PASSWORD via SMS
        #send_sms(phone, message=f"Sizning login: {user.phone} va parolingiz: {password}")

        return {"phone": phone, "password": password}