from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.serializers import AccountSerializer
from accounts.models import Account


class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
