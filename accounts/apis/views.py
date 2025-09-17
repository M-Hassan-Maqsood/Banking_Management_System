from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from accounts.apis.permissions import IsStaffUser
from accounts.serializers import AccountSerializer
from accounts.models import Account


class AccountListCreateAPIView(ListCreateAPIView):
    serializer_class = AccountSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["branch__bank__name", "account_type", "branch__bank__is_islamic"]
    search_fields = ["user__first_name", "user__last_name", "user__username"]
    ordering_fields = ["balance", "created_at", "user__username"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()

        return Account.objects.filter(user = self.request.user)


class AccountBalanceUpdateAPIView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        account = super().get_object()
        if self.request.user.is_staff or account.user == self.request.user:
            return account
        raise PermissionDenied("You are not allowed to access this account")


class StaffAccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsStaffUser]
