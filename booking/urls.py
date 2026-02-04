from django.urls import path
from .views import CreateBookingView,AdvertiserBookings,OwnerBookings

urlpatterns = [
    path('space/booking/',CreateBookingView.as_view()),
    path('advertiser/bookings/',AdvertiserBookings.as_view()),
    path('owner/bookings/',OwnerBookings.as_view()),
]
