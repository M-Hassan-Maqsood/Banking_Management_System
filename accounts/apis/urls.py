from django.urls import path

from accounts.apis.views import AccountListCreateAPIView, AccountBalanceUpdateAPIView, StaffAccountDetailAPIView


urlpatterns = [
    path("", AccountListCreateAPIView.as_view(), name = "account-list-create-api"),
    path("<int:pk>/balance/", AccountBalanceUpdateAPIView.as_view(), name = "account-balance-api"),
    path("<int:pk>/", StaffAccountDetailAPIView.as_view(), name = "staff-detail-api"),
]
