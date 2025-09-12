from django.urls import path

from banks.apis.views import BankListCreateAPIView,BankDetailAPIView


urlpatterns = [
    path("", BankListCreateAPIView.as_view(), name = "banks-list-create"),
    path("<int:pk>/", BankDetailAPIView.as_view(), name = "banks-detail"),
]
