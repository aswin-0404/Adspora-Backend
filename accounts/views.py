from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer,Loginserializer
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class Registerview(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Registration successfull"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Loginview(APIView):
    def post(self,request):
        serializer=Loginserializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']

            user=authenticate(username=email,password=password)

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
