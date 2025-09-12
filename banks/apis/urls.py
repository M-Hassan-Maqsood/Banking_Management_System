from django.urls import path, include
from rest_framework import routers

from banks.apis.views import BankListAPIView,BankViewSet, BankGenericApiView

router = routers.DefaultRouter()
router.register("banks/viewset-apis", BankViewSet, basename = "bank-viewset")

urlpatterns = [
    path("banks/apis-view", BankListAPIView.as_view(), name = "banks-apis"),
    path("banks/generic-apis", BankGenericApiView.as_view(), name = "banks-generic"),

    path("", include(router.urls)),
]
