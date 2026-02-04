from django.db import models
from accounts.models import User
from spaceowner.models import AdvertisementSpace

# Create your models here.

class Booking(models.Model):
    advertiser=models.ForeignKey(User,on_delete=models.CASCADE)
    space=models.ForeignKey(AdvertisementSpace,on_delete=models.CASCADE)
    months=models.IntegerField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    proof=models.ImageField(upload_to='payments/')
    status=models.CharField(max_length=50,choices=[
        ("PENDING","PENDING"),
        ("CONFIRMED","CONFIRMED"),
        ("REJECTED","REJECTED")
    ],
    default="PENDING")
    created_at=models.DateTimeField(auto_now_add=True)