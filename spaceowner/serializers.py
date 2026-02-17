from rest_framework import serializers
from .models import SpaceImages,AdvertisementSpace
from accounts.models import User
from booking.models import Booking
from booking.serializers import BookingDetailsSerializer

# SPACE ADD SERIALIZER

class AdvertisementSpaceAddSerializer(serializers.ModelSerializer):
    images=serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    class Meta:
        model=AdvertisementSpace
        fields=['title','space_type','location','size','price','description','images']

    def create(self, validated_data):
        image=validated_data.pop('images')
        user=self.context["request"].user

        space=AdvertisementSpace.objects.create(owner=user,**validated_data)

        for img in image:
            SpaceImages.objects.create(space=space,image=img)
            
        return space

# SPACE GETTING SERIALIZER
class SpaceImageSerializer(serializers.ModelSerializer):
    image=serializers.CharField(source='image.url')

    class Meta:
        model=SpaceImages
        fields=['image']

class SpaceOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email']

class SpaceGetserializer(serializers.ModelSerializer):
    images=SpaceImageSerializer(many=True,read_only=True)
    owner=SpaceOwnerSerializer(read_only=True)
    booking_details=serializers.SerializerMethodField()

    class Meta:
        model=AdvertisementSpace
        fields=['id','title','space_type','location','size','price','description','is_approved','images','created_at','booked','owner','booking_details']


    def get_booking_details(self,obj):
        if not obj.booked:
            return None
        
        booking=Booking.objects.filter(status="CONFIRMED").order_by('-created_at').first()

        if booking:
            return {
                "months":booking.months,
                "booked_at":booking.created_at
            }
        
        return None

class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=['status']





