from rest_framework import serializers
from accounts.models import Account
from banks.serializers import BankNameSerializer


class AccountSerializer(serializers.ModelSerializer):
    bank_name = BankNameSerializer(source = "branch.bank", read_only = True)

    class Meta:
        model = Account
        fields = "__all__"
