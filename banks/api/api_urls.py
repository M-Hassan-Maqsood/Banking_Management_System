from django.urls import path, include
from rest_framework import routers

from banks.api.api_views import BankListAPIView,BankViewSet, BankGenericView

router = routers.DefaultRouter()
router.register("banks/viewset/", BankViewSet, basename = "bank-viewset")

urlpatterns = [
    path("banks/api-view", BankListAPIView.as_view(), name = "banks-api"),
    path("banks/generic/", BankGenericView.as_view(), name = "banks-generic"),

    path("", include(router.urls)),
]
