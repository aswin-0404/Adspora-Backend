from django.db import models
from accounts.models import User
from spaceowner.models import AdvertisementSpace

# Create your models here.
class ChatRoom(models.Model):
    space=models.ForeignKey(AdvertisementSpace,on_delete=models.CASCADE,related_name='chat_rooms')
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner_chatroom')
    advertiser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='advertiser_chatroom')
    created_at=models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='message')
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    text=models.TextField()
    time_stamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}-{self.text[:20]}"




