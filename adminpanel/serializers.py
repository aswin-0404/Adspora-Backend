from rest_framework import serializers
from accounts.models import User
from spaceowner.models import AdvertisementSpace

class TopContributerSerializer(serializers.ModelSerializer):
    total_amount=serializers.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        model=User
        fields=['id','name','email','total_amount']


# _____USER MANAGEMENT______

class AllUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','is_suspend','role']


# _____SPACE MANAGEMENT______
class AllSpaceGetSerializer(serializers.ModelSerializer):

    owner=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="name"
    )

    class Meta:
        model=AdvertisementSpace
        fields=['id','title','owner','location','price','is_approved']


class OwnerDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['name','email','phone']
        read_only_fields=['name','email','phone']

