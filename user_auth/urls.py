from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token 


urlpatterns = [
  # path('login/',views.LoginAPIView.as_view()),# throtling works in this url
  path('login/',obtain_auth_token), #DRF's built-in Token Authentication view.don't need to write your own LoginAPIView for basic token generation
  path('register/',views.UserRegistration.as_view()),
  path('logout/',views.LogoutAPIView.as_view())
]