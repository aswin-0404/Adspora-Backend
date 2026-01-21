from django.urls import path
from .views import SpaceaddView,GetspaceView,OwnerProfileview

urlpatterns = [
    path('add/space/',SpaceaddView.as_view()),
    path('get/space/',GetspaceView.as_view()),
    path('owner/profile/',OwnerProfileview.as_view()),
]
