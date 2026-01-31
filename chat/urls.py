from django.urls import path
from .views import CreateChatroomView,ChatMessageListView,OwnerInboxView,AdvertiserInboxView,MarkMessageRead,InboxCount,RoomMessageCount
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('chat/room/',CreateChatroomView.as_view()),
    path('chat/messages/<int:room_id>/',ChatMessageListView.as_view()),
    path('chat/mark-read/<int:room_id>/',csrf_exempt(MarkMessageRead.as_view())),
    path('Notread/count/',InboxCount.as_view()),
    path('message/count/<int:room_id>/',RoomMessageCount.as_view()),

    # Owner URLS
    path('chat/owner/inbox/',OwnerInboxView.as_view()),


    # advertiser URLS

    path('chat/advertiser/inbox/',AdvertiserInboxView.as_view()),

]
