from django.urls import path
from .views import UserSpaceView,SpaceDetailview,Advertiserprofileview,WishlistHandleview,WishlistCount,GetWishlistView,AISearchView

urlpatterns = [
    path('spaces/',UserSpaceView.as_view()),
    path('spaces/<int:space_id>/',SpaceDetailview.as_view()),
    path('advertiser/profile/',Advertiserprofileview.as_view()),

    path('wishlist/<int:space_id>/',WishlistHandleview.as_view()),
    path('wishlist/count/',WishlistCount.as_view()),
    path('wishlist/',GetWishlistView.as_view()),

#     path('ai-search/',AISearchView.as_view()),
]
