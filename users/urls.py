from django.urls import path
from users.views import  login_view, logout_view
from . import views


app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
]
