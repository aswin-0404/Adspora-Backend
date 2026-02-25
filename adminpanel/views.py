from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from spaceowner.models import AdvertisementSpace
from booking.models import Booking
from django.db.models import Count,Sum
from django.db.models.functions import ExtractMonth
from .serializers import TopContributerSerializer,AllUserGetSerializer,AllSpaceGetSerializer,OwnerDetailsSerializer,AdminRegisterSerializer
from booking.serializers import BookingDetailsSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.mail import send_mail




# Create your views here.

#___________ADMIN DASHBOARD_________

class UserCountView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        count=User.objects.exclude(is_superuser=True).count()
        return Response({"count":count})


class ApprovedSpaceCount(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        count=AdvertisementSpace.objects.filter(is_approved=True).count()
        return Response({"count":count})
    
class NumberofBookingView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        count=Booking.objects.aggregate(count=Count('id'))
        return Response(count)
    
class TotalRevenueView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        revenue=Booking.objects.aggregate(sum=Sum('platform_fee'))
        return Response(revenue)
    

class RevenuePerMonth(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        revenue=Booking.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(revenue=Sum('amount')).order_by('month')
        return Response(revenue)
    

class TopContributerView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):

        users=User.objects.annotate(total_amount=Sum('bookings__amount')).filter(total_amount__isnull=False).order_by('-total_amount')

        serializer=TopContributerSerializer(users,many=True)
        return Response(serializer.data)



# _____USER MANAGEMENT______
class AddUSerView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer=AdminRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()

            # send_mail(
            #     subject=f"Account Created at Adspora",
            #     message=f"{user.name} Admin Got created a account for you.Now you can utilise the services of adspora.Thankyou!",
            #     from_email="adspora@gmail.com",
            #     recipient_list=[user.email],
            #     fail_silently=False
            # )
            return Response({"message":"user created succefully"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)

class UserGetView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        data=User.objects.exclude(is_superuser=True)

        serializer=AllUserGetSerializer(data,many=True)
        return Response(serializer.data)


class DeleteUser(APIView):
    permission_classes=[IsAdminUser]

    def delete(self,request,pk):
        try:
            user= User.objects.get(pk=pk)
            user.delete()

            # send_mail(
            #     subject=f"Account Deleted",
            #     message=f"Your account is Permenetly deleted by the admin!",
            #     from_email="adspora@gmail.com",
            #     recipient_list=[user.email],
            #     fail_silently=False
                
            # )
            return Response({"message":"user deleted successfully"},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"user not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        
class StatusToggle(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            user=User.objects.get(pk=pk)

            user.is_suspend= not user.is_suspend
            user.save()

            # user_status=None
            # if user.is_suspend==True:
            #     user_status="Suspended"
            # elif user.is_suspend==False:
            #     user_status="Access Aproved"

            # send_mail(
            #     subject=f"Access changed by Admin",
            #     message=f"your Account {user_status} by the admin!",
            #     from_email="adspora@gmail.com",
            #     recipient_list=[user.email],
            #     fail_silently=False
            # )
            return Response({"message":"user status updated",
                             "status":user.is_suspend},status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message":"user not exist"},status=status.HTTP_400_BAD_REQUEST)
        

# ______space management______

class GetAllSpacesView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        spaces=AdvertisementSpace.objects.all()
        serializer=AllSpaceGetSerializer(spaces,many=True)
        return Response(serializer.data)
    

class DeleteSpaceview(APIView):
    permission_classes=[IsAdminUser]

    def delete(self,request,pk):
        try:
            space=AdvertisementSpace.objects.get(pk=pk)
            space.delete()

            # send_mail(
            #     subject=f"Space Deleted",
            #     message=f"Your Space got  Permenetly deleted by the admin!",
            #     from_email="adspora@gmail.com",
            #     recipient_list=[space.owner.email],
            #     fail_silently=False
                
            # )
            return Response({"message":"space deleted successfully"},status=status.HTTP_200_OK)
        except AdvertisementSpace.DoesNotExist:
            return Response({"message":"space not found"},status=status.HTTP_400_BAD_REQUEST)


class ToggleStatusView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            space=AdvertisementSpace.objects.get(pk=pk)

            space.is_approved = not space.is_approved
            space.save()

            # space_status=None
            # if space.is_approved==True:
            #     space_status="Listing Approved"
            # elif space.is_approved==False:
            #     space_status="Listing denied"

            # send_mail(
            #     subject=f"Listing changed by Admin",
            #     message=f"your Space {space_status} by the admin!",
            #     from_email="adspora@gmail.com",
            #     recipient_list=[space.owner.email],
            #     fail_silently=False
            # )
            return Response({"message":"Space Status got changed",
                             "is_approved":space.is_approved},status=status.HTTP_200_OK)
        
        except AdvertisementSpace.DoesNotExist:
            return Response({"message":"space not available"},status=status.HTTP_400_BAD_REQUEST)

class DetailsOfOwner(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request,pk):
        try:
            ad_space=AdvertisementSpace.objects.get(pk=pk)

            no_of_listing=AdvertisementSpace.objects.filter(owner=ad_space.owner).count()

            serializer=OwnerDetailsSerializer(ad_space.owner)

            return Response({"Owner":serializer.data,
                            "listings":no_of_listing},status=status.HTTP_200_OK)
        except AdvertisementSpace.DoesNotExist:
            return Response({"message":"Not found"},status=status.HTTP_400_BAD_REQUEST)
    
# _________Bookingmanagent________


class BookingDetailView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        data=Booking.objects.all()
        serializer=BookingDetailsSerializer(data,many=True)
        return Response(serializer.data)

class AcceptBooking(APIView):
    permission_classes=[IsAdminUser]

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

class RejectBookingView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            booking=Booking.objects.get(pk=pk)
            booking.status="REJECTED"
            booking.save()
            return Response({"message":"booking rejected"},status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"message":"booking not found"},status=status.HTTP_400_BAD_REQUEST)

