from django.urls import path
from .views import UserCountView,ApprovedSpaceCount,NumberofBookingView,TotalRevenueView,RevenuePerMonth,TopContributerView,AddUSerView,UserGetView,DeleteUser,StatusToggle,GetAllSpacesView,DeleteSpaceview,ToggleStatusView,DetailsOfOwner,BookingDetailView,RejectBookingView,AcceptBooking

urlpatterns = [
    path('user-count/',UserCountView.as_view()),
    path('activespace-count/',ApprovedSpaceCount.as_view()),
    path('booking-count/',NumberofBookingView.as_view()),
    path('total-revenue/',TotalRevenueView.as_view()),
    path('revenue-permonth/',RevenuePerMonth.as_view()),
    path('top-contributer/',TopContributerView.as_view()),

    path('add-user/',AddUSerView.as_view()),
    path('all-user/',UserGetView.as_view()),
    path('delete-user/<int:pk>/',DeleteUser.as_view()),
    path('toggle-user-status/<int:pk>/',StatusToggle.as_view()),


    path('get-all-spaces/',GetAllSpacesView.as_view()),
    path('delete-space/<int:pk>/',DeleteSpaceview.as_view()),
    path('toggle-space-suspend/<int:pk>/',ToggleStatusView.as_view()),
    path('detail-of-owner/<int:pk>/',DetailsOfOwner.as_view()),


    path('booking-details/',BookingDetailView.as_view()),
    path('accept-booking/<int:booking_id>/',AcceptBooking.as_view()),
    path('reject-booking/<int:pk>/',RejectBookingView.as_view()),

]
