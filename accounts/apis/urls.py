from django.urls import path

from accounts.apis.views import AccountListCreateAPIView, AccountDetailAPIView


urlpatterns = [
    path("", AccountListCreateAPIView.as_view(), name = "accounts-list-create-api"),
    path("<int:pk>/", AccountDetailAPIView.as_view(), name = "accounts-detail-api"),
]
