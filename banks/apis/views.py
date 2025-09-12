from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from banks.models import Bank
from banks.serializers import BankSerializer


class BankListCreateAPIView(ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class BankDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
