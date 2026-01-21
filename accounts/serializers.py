from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    confirmpassword=serializers.CharField(write_only=True) 
    class Meta:
        model=User
        fields=['name','email','phone','role','password','confirmpassword','adharnumber']
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
        

class Loginserializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()