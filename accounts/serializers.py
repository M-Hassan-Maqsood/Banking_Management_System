from rest_framework import serializers
from accounts.models import Account
from banks.serializers import BankNameSerializer


class AccountSerializer(serializers.ModelSerializer):
    bank_name = BankNameSerializer(source = "branch.bank", read_only = True)

    class Meta:
        model = Account
        fields = "__all__"


class AccountSummarySerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    opening_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_deposits = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_withdrawals = serializers.DecimalField(max_digits=12, decimal_places=2)
    max_txn_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    min_running_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
