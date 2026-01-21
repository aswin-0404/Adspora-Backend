from django.shortcuts import render
from rest_framework.response import Response
from .models import ChatRoom,Message
from rest_framework import status
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import ChatMessageSerializer
from spaceowner.models import AdvertisementSpace
from spaceowner.serializers import SpaceGetserializer
from django.shortcuts import get_object_or_404
from spaceowner.permissions import IsOwnerRole

# Create your views here.
class CreateChatroomView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):

        owner_id=request.data.get("owner_id")
        space_id=request.data.get("space_id")

        if not space_id or not owner_id:
            return Response({
                "error":"space_id and owner_id is required"
            },status=status.HTTP_400_BAD_REQUEST)

        advertiser=request.user

        owner=get_object_or_404(User,id=owner_id)
        space=get_object_or_404(AdvertisementSpace,id=space_id)

        room,created=ChatRoom.objects.get_or_create(space=space,owner=owner,advertiser=advertiser)

        return Response({
            "room_id":room.id,
            "created":created
        },status=status.HTTP_200_OK)
    
class ChatMessageListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,room_id):
        room=ChatRoom.objects.select_related("space", "owner", "advertiser").get(id=room_id)

        messages=Message.objects.filter(room=room).order_by("time_stamp")
        message_serializer=ChatMessageSerializer(messages,many=True)

        space_serializer=SpaceGetserializer(room.space)

        return Response(
            {
                "space":space_serializer.data,
                "messages":message_serializer.data
            },
            status=status.HTTP_200_OK)


# OWNER CHAT SETUP

class OwnerInboxView(APIView):
    permission_classes=[IsAuthenticated,IsOwnerRole]

    def get(self,request):
        rooms=(
            ChatRoom.objects.filter(owner=request.user)
            .select_related("space","advertiser")
            .prefetch_related("message")
        )

        data=[]

        for room in rooms:
            last_msg=room.message.order_by("-time_stamp").first()

            data.append(
                {
                    "room_id":room.id,
                    "space":{
                        "id":room.space.id,
                        "title":room.space.title,
                        "location":room.space.location,
                    },
                    "advertiser":{
                        "id":room.advertiser.id,
                        "name":room.advertiser.username,
                    },
                    "last_message":last_msg.text if last_msg else "",
                    "last_time":last_msg.time_stamp if last_msg else room.created_at,
                }
            )
        return Response(data)