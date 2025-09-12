from django.urls import path, include
from rest_framework import routers

from accounts.apis.views import AccountListAPIView, AccountGenericAPIView, AccountViewSet

router = routers.DefaultRouter()
router.register("accounts/viewset-apis", AccountViewSet, basename = "accounts-viewset")

urlpatterns = [
    path("accounts/apis-view", AccountListAPIView.as_view(), name = "accounts-apis"),
    path("accounts/generic-apis", AccountGenericAPIView.as_view(), name = "accounts-generic"),

    path("", include(router.urls)),
]
