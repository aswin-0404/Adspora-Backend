from django.db import models
from accounts.models import User
from spaceowner.models import AdvertisementSpace

# Create your models here.

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    space=models.ForeignKey(AdvertisementSpace,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user','space')