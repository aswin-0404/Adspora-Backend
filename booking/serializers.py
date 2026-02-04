from rest_framework import serializers
from .models import Booking

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=["space","months","proof"]
    
    def create(self,validated_data):
        space=validated_data["space"]
        months=validated_data["months"]

        validated_data["amount"]=space.price*months+50

        return super().create(validated_data)


class BookingDetailsSerializer(serializers.ModelSerializer):
    space_title=serializers.CharField(source="space.title",read_only=True)
    space_owner=serializers.CharField(source="space.owner.name",read_only=True)
    advertiser_name=serializers.CharField(source="advertiser.name",read_only=True)
    class Meta:
        model=Booking
        fields=['id','space_title','months','amount','status','space_owner','created_at','advertiser_name']
