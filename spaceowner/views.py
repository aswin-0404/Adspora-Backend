from django.shortcuts import render
from rest_framework.response import Response
from .serializers import AdvertisementSpaceAddSerializer,SpaceGetserializer,UpdateStatusSerializer
from rest_framework.views import APIView
from .permissions import IsOwnerRole
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AdvertisementSpace
from accounts.models import User
from advertiser.serializers import AdvertiserProfileserializer
from booking.models import Booking
from django.shortcuts import get_object_or_404
from spaceowner.models import AdvertisementSpace
from django.db import transaction

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
        spaces=AdvertisementSpace.objects.filter(owner=request.user).prefetch_related('images','bookings')
        serializer=SpaceGetserializer(spaces,many=True)
        return  Response(serializer.data,status=status.HTTP_200_OK)
    
class OwnerProfileview(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def get(self,request):
        owner=User.objects.get(id=request.user.id)
        serializer=AdvertiserProfileserializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)


class OwnerSpaceDelete(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,space_id):

        try:
            space=AdvertisementSpace.objects.get(id=space_id,owner=request.user)
            space.delete()
            return Response({"message":"Space removed successfully!"},status=status.HTTP_204_NO_CONTENT)
        except AdvertisementSpace.DoesNotExist:
            return Response({"error":"Space doesnt exist"},status=status.HTTP_400_BAD_REQUEST)


class AcceptBookingview(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def patch(self,request,booking_id):
        booking=get_object_or_404(Booking,id=booking_id)

        if booking.status!="PENDING":
            return  Response({"error":"Booking already Proceed"},status=status.HTTP_400_BAD_REQUEST)
            
        with transaction.atomic():

            booking.status="CONFIRMED"
            booking.save()

            space=booking.space
            space.booked=True
            space.save()
            return Response({"message":"Status Updated succesfully"},status=status.HTTP_200_OK)
        
class BookingRequestCount(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def get(self,reqeust):
        count=Booking.objects.filter(space__owner=reqeust.user,status="PENDING").count()
        return Response({"count":count},status=status.HTTP_200_OK)
    

