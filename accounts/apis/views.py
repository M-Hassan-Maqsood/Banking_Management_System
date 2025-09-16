from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied

from accounts.apis.permissions import IsStaffUser
from accounts.serializers import AccountSerializer
from accounts.models import Account


class AccountListCreateAPIView(ListCreateAPIView):
    serializer_class = AccountSerializer
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
