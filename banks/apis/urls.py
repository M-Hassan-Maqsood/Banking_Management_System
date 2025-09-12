from django.urls import path, include
from rest_framework import routers

from banks.apis.views import BankListAPIView,BankViewSet, BankGenericAPIView

router = routers.DefaultRouter()
router.register("viewset-apis", BankViewSet, basename = "bank-viewset")

urlpatterns = [
    path("apis-view", BankListAPIView.as_view(), name = "banks-apis"),
    path("generic-apis", BankGenericAPIView.as_view(), name = "banks-generic"),

    path("", include(router.urls)),
]
