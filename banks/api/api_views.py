from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Count

from banks.models import Bank
from banks.serializers import BankSerializer


class BankListAPIView(APIView):
    def get(self, request):
        banks = Bank.objects.all().annotate(branch_count = Count("branches"))
        serializer = BankSerializer(banks, many = True)
        return Response(serializer.data)


class BankGenericView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
