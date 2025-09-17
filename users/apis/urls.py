from django.urls import path

from users.apis.views import  LoginAPIView


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name = "login"),
]
