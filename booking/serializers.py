from rest_framework import serializers
from .models import Booking
from decimal import Decimal

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=["space","months","proof","amount","platform_fee"]
        read_only_fields=["amount","platform_fee"]

    
    
    def create(self,validated_data):
        space=validated_data["space"]
        months=validated_data["months"]

        total=Decimal(space.price)*Decimal(months)

        platform_fee=total* Decimal("0.02")

        validated_data["platform_fee"]=platform_fee
        validated_data["amount"]=total-platform_fee

        return super().create(validated_data)


class BookingDetailsSerializer(serializers.ModelSerializer):
    space_title=serializers.CharField(source="space.title",read_only=True)
    space_owner=serializers.CharField(source="space.owner.name",read_only=True)
    advertiser_name=serializers.CharField(source="advertiser.name",read_only=True)

    created_at=serializers.DateTimeField(format="%d-%m-%Y", read_only=True)
    class Meta:
        model=Booking
        fields=['id','space_title','months','amount','status','space_owner','created_at','advertiser_name']
