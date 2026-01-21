from rest_framework import serializers
from .models import Message


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_id=serializers.IntegerField(source="sender.id",read_only=True)
    class Meta:
        model=Message
        fields=["id","sender_id","text","time_stamp","is_read"]