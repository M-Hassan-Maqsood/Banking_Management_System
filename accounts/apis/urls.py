from django.urls import path, include
from rest_framework import routers

from accounts.apis.views import AccountListAPIView, AccountGenericAPIView, AccountViewSet

router = routers.DefaultRouter()
router.register("viewset-api", AccountViewSet, basename = "accounts-viewset")

urlpatterns = [
    path("api-view", AccountListAPIView.as_view(), name = "accounts-apis"),
    path("generic-api", AccountGenericAPIView.as_view(), name = "accounts-generic"),

    path("", include(router.urls)),
]
