from django.db import models
from accounts.models import User
from spaceowner.models import AdvertisementSpace
from cloudinary.models import CloudinaryField

# Create your models here.

class Booking(models.Model):
    advertiser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings')
    space=models.ForeignKey(AdvertisementSpace,on_delete=models.CASCADE,related_name='bookings')
    months=models.IntegerField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    platform_fee=models.DecimalField(max_digits=10,decimal_places=2,default=2000.00)
    proof=CloudinaryField('image')
    status=models.CharField(max_length=50,choices=[
        ("PENDING","PENDING"),
        ("CONFIRMED","CONFIRMED"),
        ("REJECTED","REJECTED")
    ],
    default="PENDING")
    created_at=models.DateTimeField(auto_now_add=True)