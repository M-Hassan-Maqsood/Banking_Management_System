from django.urls import path
from accounts.views import AccountListView


app_name = "accounts"

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name = "account_list"),
]
