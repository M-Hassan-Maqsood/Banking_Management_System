from django.urls import path

from accounts.apis.views import AccountListCreateAPIView, AccountBalanceUpdateAPIView, StaffAccountDetailAPIView, AccountSummaryAPIView, CrossBankAnalyticsAPIView


urlpatterns = [
    path("", AccountListCreateAPIView.as_view(), name = "account-list-create-api"),
    path("<int:pk>/balance/", AccountBalanceUpdateAPIView.as_view(), name = "account-balance-api"),
    path("<int:pk>/", StaffAccountDetailAPIView.as_view(), name = "staff-detail-api"),
    path("reports/<int:pk>/summary/", AccountSummaryAPIView.as_view(), name = "account-summary-api"),
    path("reports/cross-bank/", CrossBankAnalyticsAPIView.as_view(), name = "cross-bank-analytics-api"),
]
