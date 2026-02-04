from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from advertiser.permissions import IsAdvertiserRole
from spaceowner.permissions import IsOwnerRole
from .serializers import BookingCreateSerializer,BookingDetailsSerializer
# Create your views here.


class CreateBookingView(APIView):
    permission_classes=[IsAuthenticated,IsAdvertiserRole]

    def post(self,request):
        serializer=BookingCreateSerializer(data=request.data)

        if serializer.is_valid():
            booking=serializer.save(advertiser=request.user)
            return Response({"booking_id":booking.id,"status":booking.status,"amount":booking.amount},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AdvertiserBookings(APIView):
    permission_classes=[IsAuthenticated,IsAdvertiserRole]

    def get(self,request):
        data=Booking.objects.filter(advertiser=request.user).select_related('space')
        serializer=BookingDetailsSerializer(data,many=True)
        return Response(serializer.data)
    

class OwnerBookings(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def get(self,request):
        data=Booking.objects.filter(space__owner=request.user).select_related('space','advertiser')
        serializer=BookingDetailsSerializer(data,many=True)

        return Response(serializer.data)
    