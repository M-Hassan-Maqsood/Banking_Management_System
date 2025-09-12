from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountListAPIView(APIView):
    def get(self, request):
        accounts = Account.objects.all().select_related("branch__bank")
        serializer = AccountSerializer(accounts, many = True)
        return Response(serializer.data)


class AccountGenericView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
