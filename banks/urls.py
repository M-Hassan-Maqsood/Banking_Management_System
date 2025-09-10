from django.urls import path
from banks.views import BankListView


app_name = "banks"

urlpatterns = [
    path("banks/", BankListView.as_view(), name = "bank_list"),
]