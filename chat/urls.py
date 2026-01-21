from django.urls import path
from .views import CreateChatroomView,ChatMessageListView,OwnerInboxView


urlpatterns = [
    path('chat/room/',CreateChatroomView.as_view()),
    path('chat/messages/<int:room_id>/',ChatMessageListView.as_view()),

    # ownerchat urls
    path('chat/owner/inbox/',OwnerInboxView.as_view()),

]
