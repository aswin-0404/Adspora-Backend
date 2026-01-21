from django.urls import path
from .views import UserSpaceView,Advertiserprofileview,WishlistHandleview,WishlistCount,GetWishlistView

urlpatterns = [
    path('spaces/',UserSpaceView.as_view()),
    path('advertiser/profile/',Advertiserprofileview.as_view()),

    path('wishlist/<int:space_id>/',WishlistHandleview.as_view()),
    path('wishlist/count/',WishlistCount.as_view()),
    path('wishlist/',GetWishlistView.as_view()),
]
