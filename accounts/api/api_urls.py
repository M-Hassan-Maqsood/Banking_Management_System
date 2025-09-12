from django.urls import path, include
from rest_framework import routers

from accounts.api.api_views import AccountListAPIView, AccountGenericView, AccountViewSet

router = routers.DefaultRouter()
router.register("accounts/viewset", AccountViewSet, basename = "accounts")

urlpatterns = [
    path("accounts/api-view", AccountListAPIView.as_view(), name = "accounts-api"),
    path("accounts/generic/", AccountGenericView.as_view(), name = "accounts-generic"),

    path("", include(router.urls)),
]
