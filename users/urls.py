from django.urls import path
from users.views import login_view, logout_view


app_name = "users"

urlpatterns = [
    path("", login_view, name = "login"),
    path("", logout_view, name = "logout"),
]
