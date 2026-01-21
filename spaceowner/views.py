from django.shortcuts import render
from rest_framework.response import Response
from .serializers import AdvertisementSpaceAddSerializer,SpaceGetserializer
from rest_framework.views import APIView
from .permissions import IsOwnerRole
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AdvertisementSpace
from accounts.models import User
from advertiser.serializers import AdvertiserProfileserializer


# Create your views here.
class SpaceaddView(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]


    def post(self,request):
        serializer=AdvertisementSpaceAddSerializer(data=request.data,context={"request":request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Space added successfully"},
            status=status.HTTP_201_CREATED
            )


class GetspaceView(APIView):
    permission_classes=[IsOwnerRole,IsAuthenticated]

    def get(self,request):
        spaces=AdvertisementSpace.objects.filter(owner=request.user).prefetch_related('images')
        serializer=SpaceGetserializer(spaces,many=True)
        return  Response(serializer.data,status=status.HTTP_200_OK)
    
class OwnerProfileview(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def get(self,request):
        owner=User.objects.get(id=request.user.id)
        serializer=AdvertiserProfileserializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)