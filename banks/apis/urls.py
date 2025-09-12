from django.urls import path, include
from rest_framework import routers

from banks.apis.views import BankListAPIView,BankViewSet, BankGenericAPIView

router = routers.DefaultRouter()
router.register("viewset-api", BankViewSet, basename = "bank-viewset")

urlpatterns = [
    path("api-view", BankListAPIView.as_view(), name = "banks-apis"),
    path("generic-api", BankGenericAPIView.as_view(), name = "banks-generic"),

    path("", include(router.urls)),
]
