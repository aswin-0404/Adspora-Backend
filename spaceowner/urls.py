from django.urls import path
from .views import SpaceaddView,GetspaceView,OwnerProfileview,OwnerSpaceDelete,AcceptBookingview,BookingRequestCount

urlpatterns = [
    path('add/space/',SpaceaddView.as_view()),
    path('get/space/',GetspaceView.as_view()),
    path('owner/profile/',OwnerProfileview.as_view()),
    path('ownerspace/delete/<int:space_id>/',OwnerSpaceDelete.as_view()),
    path('bookings/<int:booking_id>/accept/',AcceptBookingview.as_view()),
    path('booking/request/count/',BookingRequestCount.as_view()),
]
