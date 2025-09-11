from django.urls import path
from users import views


app_name = "users"

urlpatterns = [
    path("", views.login_view, name = "login"),
    path("", views.logout_view, name = "logout"),
]
