from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer,Loginserializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
# Create your views here.

class Registerview(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Registration successfull"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Loginview(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=Loginserializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']

            user=authenticate(username=email,password=password)
            print("this is the user",user)
            if  not user:
                return Response({"message":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)

            if user.is_suspend:
                return Response({"message":"Your account got suspended"},status=status.HTTP_403_FORBIDDEN)
            
            refresh=RefreshToken.for_user(user)
            access=refresh.access_token
            return Response({"message":"Login succesfull",
                             "token":{
                                "access":str(access),
                                "refresh":str(refresh)
                             },
                             "user":{
                                 "id":user.id,
                                 "name":user.name,
                                 "email":user.email,
                                 "role":user.role,
                                 "status":user.is_suspend
                             }                       
                             },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# PASSWORD RESET

class ForgotPassword(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        email=request.data.get("email")

        try:
            user=User.objects.get(email=email)

            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)

            reset_link=f"http://localhost:5173/reset-password/{uid}/{token}/"

            send_mail(
                "password Reset",
                f"click the link to reset password:\n{reset_link}",
                "adspora@gmail.com",
                [email]
            )
            return Response({"message":"Reset link sent"})
        
        except User.DoesNotExist:
            return Response({"error":"User not Found"},status=status.HTTP_400_BAD_REQUEST)
        
class ResetPassword(APIView):
    permission_classes=[AllowAny]

    def post(self,request,uid,token):
        password=request.data.get("password")

        try:
            user_id=urlsafe_base64_decode(uid).decode()
            user=User.objects.get(id=user_id)

            if default_token_generator.check_token(user,token):
                user.set_password(password)
                user.save()

                return Response({"message":"password Reset successful"})
            
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return Response({"error","invalid request"},status=status.HTTP_400_BAD_REQUEST)