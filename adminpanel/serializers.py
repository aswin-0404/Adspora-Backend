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


class AdminRegisterSerializer(serializers.ModelSerializer):
    confirmpassword=serializers.CharField(write_only=True) 
    class Meta:
        model=User
        fields=['name','email','phone','role','password','confirmpassword','adharnumber','is_suspend']
        extra_kwargs={
            "password":{'write_only':True}
        }

    def validate_email(self,value):
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Email Format is incorrect")
        return value
    
    def validate_password(self,value):
        if len(value) <8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate(self, data):
        if data['password'] != data['confirmpassword']:
            raise serializers.ValidationError({
                "confirmpassword": "Passwords do not match"
            })
        return data


    
    def validate_adharnumber(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Aadhaar number must be 12 digits")
        return value

    
    def create(self, validated_data):
        validated_data.pop('confirmpassword')
        user=User.objects.create_user(**validated_data)
        return user