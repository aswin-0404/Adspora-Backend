from django.urls import path
from .views import Registerview,Loginview,ForgotPassword,ResetPassword,ProfileEditView

urlpatterns = [
    path('register/',Registerview.as_view()),
    path('login/',Loginview.as_view()),
    path('forgot-password/',ForgotPassword.as_view()),
    path('reset-password/<uid>/<token>/',ResetPassword.as_view()),

    path('edit-profile/',ProfileEditView.as_view()),
]
