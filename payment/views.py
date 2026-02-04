from django.shortcuts import render
import razorpay
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from spaceowner.models import AdvertisementSpace
from rest_framework import status
from booking.models import Booking
# Create your views here.

client=razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

class CreatePaymentOrder(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        space_id=request.data["space"]
        months=int(request.data["months"])

        space=AdvertisementSpace.objects.get(id=space_id)
        amount=space.price*months+50

        order=client.order.create({
            "amount":int(amount*100),
            "currency":"INR"
        })

        return Response({
            "order_id":order["id"],
            "amount":amount,
            "key":os.getenv("RAZORPAY_KEY_ID")
        })
    

class VerifyPayment(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id":request.data["order_id"],
                "razorpay_payment_id":request.data["payment_id"],
                "razorpay_signature":request.data["signature"],
            })
        except:
            return Response({"error":"payment verification Failed!"},status=status.HTTP_400_BAD_REQUEST)
        
        Booking.objects.create(
            advertiser=request.user,
            space_id=request.data["space"],
            months=request.data["months"],
            amount=request.data["amount"],
            status="CONFIRMED"
        )

        return Response({"status":"payment Verified and booking Confirmed"},status=status.HTTP_201_CREATED)