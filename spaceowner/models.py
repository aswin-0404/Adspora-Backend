from django.db import models
from accounts.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class AdvertisementSpace(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    space_type=models.CharField(max_length=50)
    location=models.CharField(max_length=150)
    size=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    booked=models.BooleanField(default=False)

class SpaceImages(models.Model):
    space=models.ForeignKey(AdvertisementSpace,related_name="images",on_delete=models.CASCADE)
    image=CloudinaryField('image')
