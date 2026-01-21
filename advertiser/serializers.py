from accounts.models import User
from rest_framework import serializers
from spaceowner.serializers import SpaceGetserializer
from .models import Wishlist

class AdvertiserProfileserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','name','phone','adharnumber']
        extra_kwargs={
            'email':{'read_only':True},
            'adharnumber':{'read_only':True}
        }


# WISHLIST

class Wishlistserializer(serializers.ModelSerializer):
    space=SpaceGetserializer(read_only=True)
    class Meta:
        model=Wishlist
        fields=['id','space','created_at']