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
from advertiser.permissions import IsAdvertiserRole
from django.db.models import Max
from django.db.models import Count
from django.db.models import Q

from chat.authentication import CsrfExemptJWTAuthentication



# Create your views here.
class CreateChatroomView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):

        owner_id=request.data.get("owner_id")
        space_id=request.data.get("space_id")
        text=request.data.get("text")

        if not all([space_id, owner_id, text]):
            return Response(
                {"error": "space_id, owner_id and text are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertiser=request.user

        owner=get_object_or_404(User,id=owner_id)
        space=get_object_or_404(AdvertisementSpace,id=space_id)

        room,created=ChatRoom.objects.get_or_create(space=space,owner=owner,advertiser=advertiser)

        Message.objects.create(
            room=room,
            sender=advertiser,
            text=text
        )

        return Response({
            "room_id":room.id,
            "created":created
        },status=status.HTTP_200_OK)
    


class ChatRoomExist(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        space_id=request.GET.get("space")
        owner_id=request.GET.get("owner")

        if not space_id or not owner_id:
            return Response(
                {"error":"Missing parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        room,created=ChatRoom.objects.get_or_create(
            space_id=space_id,
            owner_id=owner_id,
            advertiser=request.user
        )
        
        return Response({"room_id":room.id})
    
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
                        "name":room.advertiser.name,
                    },
                    "last_message":last_msg.text if last_msg else "",
                    "last_time":last_msg.time_stamp if last_msg else room.created_at,
                }
            )
        return Response(data)


# ADVERTISER CHAT SETUP

class  AdvertiserInboxView(APIView):
    permission_classes=[IsAuthenticated,IsAdvertiserRole]

    def get(self,request):
        advertiser=request.user

        rooms=(
            ChatRoom.objects.filter(advertiser=advertiser)
            .annotate(last_time=Max("message__time_stamp"))
            .order_by('-last_time')
        )

        data=[]

        for room in rooms:
            last_message=(
                Message.objects.filter(room=room).order_by("-time_stamp").first()
            )

            data.append({
                "room_id":room.id,
                "space":{
                    "id":room.space.id,
                    "title":room.space.title,
                },
                "owner":{
                    "id":room.owner.id,
                    "name":room.owner.name,
                },
                "last_message":last_message.text if last_message else "",
                "last_time":last_message.time_stamp if last_message else None
            })
        
        return Response(data)

class MarkMessageRead(APIView):
    authentication_classes=[CsrfExemptJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, room_id):
        user = request.user

        room = get_object_or_404(ChatRoom, id=room_id)

        # 🔐 Security: user must be part of the chat
        if user != room.owner and user != room.advertiser:
            return Response(
                {"error": "You are not allowed to access this chat"},
                status=status.HTTP_403_FORBIDDEN
            )
        print("USER:", request.user)
        print("AUTH:", request.auth)


        # Mark only incoming messages as read
        Message.objects.filter(
            room=room,
            is_read=False
        ).exclude(sender=user).update(is_read=True)

        return Response(
            {"status": "messages marked as read"},
            status=status.HTTP_200_OK
        )


class InboxCount(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        notreadcount=Message.objects.filter(
            is_read=False).exclude(
                sender=request.user).filter(
                    Q (room__owner=request.user)| Q(room__advertiser=request.user)).count()
        
        return Response({"count":notreadcount},status=status.HTTP_200_OK)

class RoomMessageCount(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,room_id):
        count=Message.objects.filter(room_id=room_id,is_read=False).exclude(sender=request.user).count()
        return Response({
            "count":count,
            'room_id':room_id
        })


