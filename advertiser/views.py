from django.shortcuts import render
from spaceowner.serializers import SpaceGetserializer
from spaceowner.models import AdvertisementSpace
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import IsAdvertiserRole
from rest_framework.permissions import IsAuthenticated
from .serializers import AdvertiserProfileserializer
from accounts.models import User
from .models import Wishlist
from .serializers import Wishlistserializer
from rest_framework.permissions import AllowAny

# Create your views here.
class UserSpaceView(APIView):
    permission_classes=[IsAdvertiserRole,IsAuthenticated]

    def get(self,request):
        space=AdvertisementSpace.objects.filter(is_approved=True).prefetch_related('images')
        serializer=SpaceGetserializer(space,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class SpaceDetailview(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,space_id):
        try:
            space=AdvertisementSpace.objects.get(id=space_id)
            serializer=SpaceGetserializer(space)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
        except AdvertisementSpace.DoesNotExist:
            return Response({"error":"space doesn't exist"})

class Advertiserprofileview(APIView):
    permission_classes=[IsAdvertiserRole,IsAuthenticated]

    def get(self,request):
        adver=User.objects.get(id=request.user.id)
        serializer=AdvertiserProfileserializer(adver)
        return Response(serializer.data,status=status.HTTP_200_OK)


# WISHLIST

class WishlistHandleview(APIView):
    permission_classes=[IsAuthenticated,IsAdvertiserRole]

    def post(self,request,space_id):
        try:
            space=AdvertisementSpace.objects.get(id=space_id)
        except AdvertisementSpace.DoesNotExist:
            return Response ({"message":"space is not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        wishlist_item,created=Wishlist.objects.get_or_create(user=request.user,space=space)

        if not created:
            wishlist_item.delete()
            return Response({"wishlisted":False,"message":"removed from wishlist"},status=status.HTTP_200_OK)
        
        return Response({"wishlisted":True,"message":"added to wishlist"},status=status.HTTP_201_CREATED)

class WishlistCount(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        count=Wishlist.objects.filter(user=request.user).count()
        return Response({"count":count})
    

class GetWishlistView(APIView):
    permission_classes=[IsAuthenticated,IsAdvertiserRole]

    def get(self,request):
        space=Wishlist.objects.filter(user=request.user)
        serializer=Wishlistserializer(space,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

# AI chat searching

from rag.rag_service import rag_search
import os
from rag.gemini_services import generate_ai_replay


class AISearchView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        query=request.data.get("query")

        spaces=rag_search(query)

        ai_replay=generate_ai_replay(query,spaces)

        return Response({
            "replay":ai_replay,
            "results":[
                {
                    "id":s.id,
                    "title":s.title,
                    "location":s.location,
                    "price":s.price,
                    "space_type":s.space_type,
                    "size":s.size,
                    "owner":{
                        "id":s.owner.id
                    },
                    "images":[
                        {
                        "id":img.id,
                        "image":img.image.url
                        }
                        for img in s.images.all()
                    ]
                }
                for s in spaces
            ]
        })